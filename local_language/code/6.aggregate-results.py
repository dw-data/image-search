#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import json
from pprint import pprint
import numpy as np
import nltk



def retrieve_safesearch_likelihood(row):
    
    # Build the path to the file with the data Cloud Vision API data
    search_query = row.search_query.replace(" ","-")
    position = row.position
        
    fpath = f"../output/vision_results/{search_query}-{position}.json"
    
    try:
        # Access the JSON file
        with open(fpath) as f:
            data = json.load(f)
            safe_search = data["safe_search_annotations"]
    except FileNotFoundError:
        # There is a weird bug when we simply return None for the first row, so we had to adapt this piece of code
        results = {
            "adult": np.nan,
            "racy": np.nan,
            "spoof": np.nan,
            "violence": np.nan,
            "medical": np.nan,
        }
        
        return pd.Series(results)
        
    results = {
        "adult": safe_search["adult"]["likelihood"],
        "racy": safe_search["racy"]["likelihood"],
        "spoof": safe_search["spoof"]["likelihood"],
        "violence": safe_search["violence"]["likelihood"],
        "medical": safe_search["medical"]["likelihood"]
    }
        
    return pd.Series(results)


def retrieve_m49_standard(df):
    '''
    Adds ISO-code, M49 code and country name data to the dataframe.
    '''
    
    # Reads the nationalities, adjectivals and demonyms csv
    nationalities = pd.read_csv("../input/nationalities.csv")
    
    # Reads and formats the CSV with the UN M49 standard classification
    m49 = pd.read_csv("../input/unsd-m49.tsv", sep='\t', dtype="str")
    
    m49 = m49[["Region Code", "Region Name", 
               "Sub-region Code", "Sub-region Name", 
               "Intermediate Region Code", "Intermediate Region Name", 
               "Country or Area", "M49 Code", "ISO-alpha3 Code"]]

    m49 = m49.rename(columns={
        "Region Code": "region_code",
        "Region Name": "region_name",
        "Sub-region Code": "sub_region_code",
        "Sub-region Name": "sub_region_name",
        "Country or Area": "country_or_area",
        "Intermediate Region Code": "intermediate_region_code",
        "Intermediate Region Name": "intermediate_region_name",
        "M49 Code": "m49_code",
        "ISO-alpha3 Code": "iso_a3"
    })
    
    # Merges them both
    nationalities = nationalities.merge(m49, left_on="country", right_on="country_or_area", how="left")
                        
    df = df.merge(nationalities, on='search_query')
    
    return df



def add_counts(df):
    '''
    Adds the count of all images fetched succesfully
    '''
    
    # Dict that will hold the count of images and results for each search query
    imgs_fetched = {}
    results_fetched = {}
    
    # For each unique query...
    for search_query in df.search_query.unique():
        
        # Compute how many images were fetched and save it into the dictionary
        img_count = df[(df.search_query == search_query) & ~(df.img_path.isna())].shape[0]
        imgs_fetched[search_query] = img_count
        
        # Do the same for the results
        results_count = df[(df.search_query == search_query)].shape[0]
        results_fetched[search_query] = results_count

    # Creates a new column by matching the search query column with the dictionaries above
    df["imgs_fetched"] = df.search_query.map(imgs_fetched)
    df["results_fetched"] = df.search_query.map(results_fetched)

    
    return df


def main():
    
    df = pd.read_csv("../output/dataset/aggregated-raw-data.csv")
    
    df = pd.concat([df, df.apply(retrieve_safesearch_likelihood, axis=1)], axis=1)
        
    df = retrieve_m49_standard(df)
        
    df.to_csv("../output/dataset/complete-data.csv", index=False)
                  
    return df


if __name__ == "__main__":
    main()

