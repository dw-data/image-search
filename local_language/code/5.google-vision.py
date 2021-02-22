#!/usr/bin/env python
# coding: utf-8

# # 5. Google Vision

# On this notebook, we will pass the downloaded images through Google's Cloud Vision API, in order to retrieve the [likelihood of each image being 'adult' or 'racy'](https://cloud.google.com/vision/docs/detecting-safe-search). 
# 
# According to [Cloud Vision's documentation](https://cloud.google.com/vision/docs/reference/rpc/google.cloud.vision.v1#google.cloud.vision.v1.SafeSearchAnnotation), a **racy** image is one that "may include (but is not limited to) skimpy or sheer clothing, strategically covered nudity, lewd or provocative poses, or close-ups of sensitive body areas". **Adult images** are more explicit. According to the docs, "Adult content may contain elements such as nudity, pornographic images or cartoons, or sexual activities."
# 
# The queries also return the likelihood for the following safe search categories: "spoof", "violence" and "medical". I don't plan to use them in the analysis, but I'll collect them nevertheless to make the most of each request.
# 
# We will also collect the [description labels](https://cloud.google.com/vision/docs/labels) of each image. Maybe I will use them to do further analysis later.
# 
# 

# In[40]:


import pandas as pd
import requests
from google.cloud import vision
import io
import json
import os
from pprint import pprint
import multiprocessing
import numpy as np
import time
from PIL import Image, UnidentifiedImageError


# In[2]:


# Globals/credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("../credentials/portrayal-of-women-cloud-vision-credentials.json")


def retrieve_image_annotations(path, search_query, position):
    
    '''
    Detects labels and safe search annotations
    for a local image. Returns the results as
    a dictionary.
    
    Params:
    path: path to image file
    search_query: the google image search string that retrieved this image
    position: the position of the image in google search results
    '''
    
    def parse(r, path, search_query, position):
        '''
        Formats the Cloud Vision API response
        in a JSON-like format.
        '''

        # Names of likelihood from google.cloud.vision.enums
        likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                           'LIKELY', 'VERY_LIKELY')


        safe_search_annotations = {

            "adult": { 
                "likelihood": likelihood_name[r["safe_search"].adult],
            },
            "racy": {
                "likelihood": likelihood_name[r["safe_search"].racy],
            },
            "spoof": {
                "likelihood": likelihood_name[r["safe_search"].spoof],
            },
            "medical": {
                "likelihood": likelihood_name[r["safe_search"].medical],
            },
            "violence": {
                "likelihood": likelihood_name[r["safe_search"].violence],
            },

        }

        label_annotations = [ ]

        for label in r["labels"]:
            label_annotations.append({
                "mid": label.mid,
                "score": float(label.score),
                "topicality": float(label.topicality),
                "description": label.description
            })

        return {
            "path": path,
            "search_query": search_query.replace(" ", "-"),
            "position": int(position),
            "label_annotations": label_annotations,
            "safe_search_annotations": safe_search_annotations
        }
    
    
    def save_json(data, search_query, position):
        '''
        Saves the parsed response as JSON file.
        '''
        
        directory = f"../output/vision_results/"
        fname = f"{search_query.replace(' ', '-')}-{position}.json"    
        fpath = f"{directory}{fname}"
                
        with open(fpath, "w+") as f:
            json.dump(data, f, indent=4)
    
    
    
    print(f"Now looking at image {path}")
    
    # Checks if file is an image. If not, raise error
    try:
        with Image.open(path) as im:
            im.verify()
    except UnidentifiedImageError:
        # Saves error message to a log
        logfile = f"../output/logs/error-{search_query.replace(' ', '-')}-{position}.txt"
        log = "File is not an image"
        
        with open(logfile, "w+") as f:
            f.write(log)
            
        raise TypeError(f"{search_query} position #{position}: file is not an image")
        
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
        
    # Check if this file was already processed. If it was, return nothing
    if os.path.isfile( f"../output/vision_results/{search_query.replace(' ', '-')}-{position}.json"):
        print(f"{search_query} position #{position} already analyzed")
        return
        
    # Sleeps to avoid surpassing API quotas
    time.sleep(.3)
    
    # Initializes API client
    client = vision.ImageAnnotatorClient()
    
    # Makes requests for label and safe search endpoints
    image = vision.Image(content=content)
    
    response = client.annotate_image({
        "image": image,
        "features": [{'type_': vision.Feature.Type.LABEL_DETECTION}, 
                     {'type_': vision.Feature.Type.SAFE_SEARCH_DETECTION}]
    })
    
    # If there's an error with the rquest
    if response.error.message:
        logfile = f"../output/logs/error-{search_query.replace(' ', '-')}-{position}.txt"
        # Saves error message to a log
        log = f"Error '{response.error.message}' on file {path}"

        with open(logfile, "w+") as f:
            f.write(log)
        
        # Raise
        raise RuntimeError("Error in Cloud Vision API request. Check log files for more information")
        
   
    # Parses response
    r = {
        "labels": response.label_annotations,
        "safe_search": response.safe_search_annotation
    }
    
    r = parse(r, path, search_query, position)
    
    # Saves the parsed response as a JSON file
    save_json(r, search_query, position)
    
    print(f"Sucessfully saved Cloud Vision data for query {search_query}, position #{position}")


# In[22]:


def analyze_images(df, axis=1):
    '''
    A wrapper function that will apply
    the function analyse_image to each 
    row of the dataframe
    '''
    
    def analyze_image(row):
        '''
        Performs the requests to the API using pandas
        df.apply methods.
        '''

        try:
            retrieve_image_annotations(row.img_path, row.search_query, row.position)
        except (TypeError, RuntimeError):
            print(f"Error on row {row.name}, check logs for more information")
            return
                

    df.apply(analyze_image, axis=axis)

# In[23]:


def parallelize(df, func):
    '''
    Runs a apply function in parallel
    by splitting the dy by as many
    CPU cores as available.
    '''
    
    # Determines the number of 
    n_cores = multiprocessing.cpu_count()
    df_split = np.array_split(df, n_cores)
    
    pool = multiprocessing.Pool(n_cores)
    pool.map(func, df_split)
    pool.close()
    pool.join()


# In[24]:


def main():
    
    # Reads the collected data
    df = pd.read_csv("../output/dataset/aggregated-raw-data.csv")
    
    # Removes the images for which the download failed
    df = df[~df.img_path.isna()]
        
    parallelize(df, analyze_images)


# In[25]:


if __name__ == "__main__":
    main()

