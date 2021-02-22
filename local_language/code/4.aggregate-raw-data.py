#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import json
import glob
import os



def read_jsons():
    '''
    Reads the JSON files with the Google Image Search results
    and stores them into a single dictionary, which is returned.
    '''
    
    # Grabs all the filepaths
    files = glob.glob("../output/search_results/*.json")
    
    # Reads all those files and save them into a new dictionary
    jsons = { }
    for file in files:
        
        with open(file) as f:
            data = json.load(f)
            
            query = data["search_parameters"]['q']
    
            results = data["images_results"]
                
            jsons[query] = results.copy()
            
    return jsons


def make_df(jsons):
    '''
    Turns a JSON-like array of dictionaries,
    produced by the function read_jsons(),
    into a single pandas datrame, which is returned.
    '''

    dfs = []
    
    # Saves both the values of each dictionary
    # and an identifying column with the respective search query
    for k,v in jsons.items():
        df = pd.DataFrame(v)
        df['search_query'] = k
        dfs.append(df)

    dfs = pd.concat(dfs, ignore_index=True)
    
    return dfs


def add_information(df):
    '''
    Adds both the local image filepath and the downloaded website 
    text to each row in the dataframe. If there is no image or text 
    file for that search result, the function fills the row with a None.
    '''
    
    def get_img_path(row):
        '''
        Fetches the local path of the image 
        downloaded for the row's search entry,
        if there is one. Returns a None if there's not.
        '''
        
        # We need to use the glob approach here to check if the file exists
        # because we can't be sure about the extension of the image file.
        pattern = f'../output/imgs/{row.search_query.replace(" ","-")}/{row.position}.*'
        files = glob.glob(pattern)
        
        if files:
            assert len(files) == 1
            img_path = files[0]
            
        else:
            img_path = None
            
        return pd.Series({"img_path": img_path})
    
    
    def get_full_title(row):
        '''
        Fetches the title tag of a given JSON file.
        '''
        
        fname = f'../output/link_contents/{row.search_query.replace(" ","-")}/{row.position}-title-tag.json'        
        
        if os.path.exists(fname):
            
            with open(fname, "r") as f:
                data = json.load(f)
                full_title = data["title"]
                
                # There is an entry with a \r in the title, which I have to remove
                full_title = full_title.replace("\r", " ")

            
        else:
            full_title = None
            
        return pd.Series({"full_title": full_title})
    
        
    df["img_path"] = df.apply(get_img_path, axis=1)
    df["full_title"] = df.apply(get_full_title, axis=1)
    
    return df



def main():
    
    jsons = read_jsons()
    df = make_df(jsons)
    df = add_information(df)
    df.to_csv("../output/dataset/aggregated-raw-data.csv", index=False)



if __name__ == "__main__":
    main()




