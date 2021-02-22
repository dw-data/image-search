#!/usr/bin/env python
# coding: utf-8

# Full title extraction
from bs4 import BeautifulSoup
import requests
import json
import glob
import os
from multiprocessing import Pool, cpu_count

# First, we will need to access the JSON files.
def glob_filepaths(pattern):
    return glob.glob(pattern)


# Then, we will need to download the text files for each URL.
def download_titles(fpath):
    '''
    Downloads the text for each linked in the JSON file
    representing the search results retrieved by SerpAPI.
    Saves the texts of a given country inside a folder with the query name.
    
    Params
    
    fpath: the path to a .json file saved at the previous notebook
    '''
    
    def download_full_title(url, position, directory):
        '''
        Helper function that downloads a single image from a URL using
        the requests module.
        
        Params
        
        url: The url to a website
        position: The position the image had in Google Image Search. Used as filename.
        '''
        
        print(f">> Fetching full title #{position} at url {url}")
        
        # If the file already exists, skip
        # pattern_a = f"{directory}/{position}-trafilatura.json"
        pattern = f"{directory}/{position}-title-tag.json"
        if os.path.exists(pattern):
            print(">> File already downloaded")
            return
        

        user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
        r = requests.get(url, 
            headers={"User-Agent": user_agent},
            timeout=10)

        if r.ok:

            soup = BeautifulSoup(r.text, "lxml")
            title = soup.title.string

            if title:
                with open(f'{directory}/{position}-title-tag.json', 'w+') as f:
                     json.dump({"title": title,
                                "url": url}, f) 
            else:
                print(f">> No titlte tag in {url}")

        else:
            print(f">> Response not succesful in {url}")

    # Redas data in
    data = json.load(open(fpath, "r"))
    
    # Creates subdirectory
    query = data["search_information"]["query_displayed"]
    query = query.replace(" ","-")

    directory = f"../output/link_contents/{query}"

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Fetch URLs
    image_results = data["images_results"]
    urls = [item["link"] for item in image_results]
    positions = [item["position"] for item in image_results]
    
    # Download them
    print(f"> Downloading text for query '{query}'")
    for url, position in zip(urls, positions):
        try:
            download_full_title(url, position, directory)
        except Exception as e:
            print(f"> Error {e} on position #{position}")


# Let's run that.
def main():

    pool = Pool(cpu_count())
    fpaths = glob_filepaths("../output/search_results/*.json")
    pool.map(download_titles, fpaths)
    pool.close()
    pool.join()



if __name__ == "__main__":
    main()

