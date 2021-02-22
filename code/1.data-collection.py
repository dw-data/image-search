#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from serpapi import GoogleSearch
import json

GoogleSearch.SERP_API_KEY = "YOUR API KEY GOES HERE"


def image_search(query, country):
    '''
    Makes a Google Image Search using SerpApi.
    The results are saved in JSON format.
    
    Params
    
    query: The terms to search for. String.
    country: This is the name of the JSON file that will be saved.
    '''
    try:
        search = GoogleSearch({"q": query.lower(), "tbm": "isch"})
        results = search.get_json()

        with open(f"../output/search_results/{country.replace(' ','-').lower()}.json", "w+") as f:
            json.dump(results, f, indent=4)
            
    except Exception as e:
        results = {"error": e}
        
        with open(f"../output/search_results/{country.replace(' ','-').lower()}.json", "w+") as f:
            json.dump(results, f, indent=4)


def main():

    nationalities = pd.read_csv("../input/nationalities.csv")

    search_queries = [ adjective + " women" for adjective in nationalities.adjectivals]

    countries = [ country for country in nationalities.country ]

    for query, country in zip(search_queries, countries):
        image_search(query, country)




if __name__ == "__main__":
    main()
