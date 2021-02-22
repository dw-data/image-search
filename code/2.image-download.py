#!/usr/bin/env python
# coding: utf-8

# # 2. Image download

# Now we have image search information about around 200 nationalities. 
# We also need to download the images in order to analyze them computationally.

import requests
from requests import ConnectionError
from requests.exceptions import ReadTimeout
from urllib3.exceptions import ReadTimeoutError
import json
import glob
import os
import shutil
from pprint import pprint
from multiprocessing import Pool, cpu_count

# We need to read all the downloaded JSON files in order to access the image list. Let's define a function to do that.
def glob_filepaths(pattern):
    return glob.glob(pattern)


# Now, we will define a function that will read each one of those to retrieve the image URLs and download the content.
def download_images(fpath):
    '''
    Downloads the images listed in the JSON file
    representing the search results retrieved by SerpAPI.
    Saves the images of a given country inside a folder with the query name.
    
    Params
    
    fpath: the path to a .json file saved at the previous notebook
    '''
    
    def download_image(url, position):
        '''
        Helper function that downloads a single image from a URL using
        the requests module.
        
        Params
        
        url: The url to an image file 
        position: The position the image had in Google Image Search. Used as filename.
        '''
        
        
        print(f">> Fetching file #{position} at url {url}")
        
        # If the file for this position already exists, skip it
        files = glob.glob(f"{directory}/{position}.*")
        if len(files) > 0:
            print(">> File already downloaded")
            return

        try:
            r = requests.get(url, stream=True, timeout=10, headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"})
            if r.status_code == 200:

                r.raw.decode_content = True

                # Determines content type
                try:
                    content_type = r.headers["content-type"]
                    extension = content_type.split("/")[1]
                except (KeyError, IndexError):
                    print(f"Can't guess file type  on url {url}, position #{position}")
                    return

                # Saves file
                with open(f'{directory}/{position}.{extension}', 'wb') as out_file:
                    shutil.copyfileobj(r.raw, out_file)

            else:
                print(f">> Status code error {r.status_code} on url {url}, position #{position}")
                
        except (ConnectionError, ReadTimeout, ReadTimeoutError):
            print(f">> Connection error found in url {url}, position #{position}")
            return
        

    print(f"Looking at fpath {fpath}")

    # Redas data in
    data = json.load(open(fpath, "r"))
    
    # Creates subdirectory
    query = data["search_information"]["query_displayed"]
    query = query.replace(" ","-")
   
    directory = f"../output/imgs/{query}" 
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Fetch image URLs
    image_results = data["images_results"]

    urls = [item["original"] for item in image_results if "original" in item.keys()]
    positions = [item["position"] for item in image_results]
    
    # Download them
    print(f"> Downloading files for query '{query}'")
    for url, position in zip(urls, positions):
        download_image(url, position)


# Now, we can run the commands in the main function using paralell processing to make things go a little faster.
def main():

    pool = Pool(cpu_count())
    fpaths = glob_filepaths("../output/search_results/*.json")
    pool.map(download_images, fpaths)
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()

