#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import json
from pprint import pprint
import numpy as np
import nltk



def retrieve_safesearch_likelihood(row):
    '''
    df.apply function that retrieves the Google Cloud Vision
    data for a given search term.
    '''
    
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
        return None
        
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
        
    # And manually fill the missing values of interest
    fill_values = [

         {'country': 'Bolivia', 'country_or_area': 'Bolivia',
          'adjectivals': 'Bolivian',
          'demonyms': 'Bolivians',
          'region_code': '019',
          'region_name': 'Americas',
          'sub_region_code': '419',
          'sub_region_name': 'Latin America and the Caribbean',
          'intermediate_region_code': '005',
          'intermediate_region_name': 'South America',
          'country_or_area': "Bolivia (Plurinational State of)",
          'm49_code': "068",
          'iso_a3': 'BOL'},

         {'country': 'Brunei','country_or_area': 'Brunei',
          'adjectivals': 'Bruneian',
          'demonyms': 'Bruneians',
          'region_code': "142",
          'region_name': "Asia",
          'sub_region_code': "035",
          'sub_region_name': "South-eastern Asia",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Brunei Darussalam",
          'm49_code': "096",
          'iso_a3': 'BRN'},

         {'country': 'Czech Republic','country_or_area': 'Czech Republic',
          'adjectivals': 'Czech',
          'demonyms': 'Czechs',
          'region_code': "150",
          'region_name': "Europe",
          'sub_region_code': "151",
          'sub_region_name': "Eastern Europe",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Czechia",
          'm49_code': "203",
          'iso_a3': 'CZE'},

         #{'country': 'East Timor','country_or_area': 'East Timor',
         # 'adjectivals': 'Timorese',
         # 'demonyms': 'Timorese',
         # 'region_code': "142",
         # 'region_name': "Asia",
         # 'sub_region_code': "035",
         # 'sub_region_name': "South-eastern Asia",
         # 'intermediate_region_code': np.nan,
         # 'intermediate_region_name': np.nan,
         # 'country_or_area': "Timor-Leste",
         # 'm49_code': "626"},

         {'country': 'England',
          'adjectivals': 'English',
          'demonyms': 'English',
          'region_code': "150",
          'region_name': "Europe",
          'sub_region_code': "154",
          'sub_region_name': "Northern Europe",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': 'England',
          'm49_code': np.nan,
          'iso_a3': 'xENG'},

         {'country': 'Iran','country_or_area': 'Iran',
          'adjectivals': 'Iranian',
          'demonyms': 'Iranians',
          'region_code': "142",
          'region_name': "Asia",
          'sub_region_code': "034",
          'sub_region_name': "Southern Asia",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Iran (Islamic Republic of)",
          'm49_code': "364",
          'iso_a3': 'IRN'},

         {'country': 'Ivory Coast','country_or_area': 'Ivory Coast',
          'adjectivals': 'Ivorian',
          'demonyms': 'Ivorians',
          'region_code': "002",
          'region_name': "Africa",
          'sub_region_code': "202",
          'sub_region_name': "Sub-Saharan Africa",
          'intermediate_region_code': "011",
          'intermediate_region_name': "Western Africa",
          'country_or_area': "Côte d’Ivoire",
          'm49_code': "384",
          'iso_a3': 'CIV'},

         {'country': 'North Korea','country_or_area': 'North Korea',
          'adjectivals': 'North Korean',
          'demonyms': 'North Koreans',
          'region_code': "142",
          'region_name': "Asia",
          'sub_region_code': "030",
          'sub_region_name': "Eastern Asia",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Democratic People's Republic of Korea",
          'm49_code': "408",
          'iso_a3': 'PRK'
         },

         {'country': 'South Korea','country_or_area': 'South Korea',
          'adjectivals': 'South Korean',
          'demonyms': 'South Koreans',
          'region_code': "142",
          'region_name': "Asia",
          'sub_region_code': "030",
          'sub_region_name': "Eastern Asia",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Republic of Korea",
          'm49_code': "410",
          'iso_a3': 'KOR'},

         {'country': 'Kosovo',
          'adjectivals': 'Kosovar',
          'demonyms': 'Kosovars',
          'region_code': "150",
          'region_name': "Europe",
          'sub_region_code': "039",
          'sub_region_name': "Southern Europe",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': 'Kosovo',
          'm49_code': np.nan,
          'iso_a3': "XKX"},

         {'country': 'Lao','country_or_area': 'Lao',
          'adjectivals': 'Laos',
          'demonyms': 'Laotians',
          'region_code': "142",
          'region_name': "Asia",
          'sub_region_code': "035",
          'sub_region_name': "South-eastern Asia",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Lao People's Democratic Republic",
          'm49_code': "418",
          'iso_a3': 'LAO'},

         {'country': 'Macau','country_or_area': 'Macau',
          'adjectivals': 'Macanese',
          'demonyms': 'Chinese',
          'region_code': "142",
          'region_name': "Asia",
          'sub_region_code': "030",
          'sub_region_name': "Eastern Asia",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "China, Macao Special Administrative Region",
          'm49_code': "446",
          'iso_a3': "MAC",
         },

         {'country': 'Micronesia','country_or_area': 'Micronesia',
          'adjectivals': 'Micronesian',
          'demonyms': 'Micronesians',
          'region_code': "009",
          'region_name': "Asia",
          'sub_region_code': "057",
          'sub_region_name': "Micronesia",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Micronesia (Federated States of)",
          'm49_code': "583",
          'iso_a3': 'FSM'
         },

         {'country': 'Moldova','country_or_area': 'Moldova',
          'adjectivals': 'Moldovan',
          'demonyms': 'Moldovans',
          'region_code': "150",
          'region_name': "Europe",
          'sub_region_code': "151",
          'sub_region_name': "Eastern Europe",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Republic of Moldova",
          'm49_code': "498",
          'iso_a3': 'MDA'
         },

         {'country': 'Northern Ireland',
          'adjectivals': 'Northern Irish',
          'demonyms': 'Northern Irish',
          'region_code': "150",
          'region_name': "Europe",
          'sub_region_code': "154",
          'sub_region_name': "Northern Europe",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': 'Northern Ireland',
          'm49_code': np.nan,
          'iso_a3': 'IRN'
         },

         {'country': 'Palestine',
          'adjectivals': 'Palestinian',
          'demonyms': 'Palestinians',
          'region_code': "142",
          'region_name': "Asia",
          'sub_region_code': "145",
          'sub_region_name': "Western Asia",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "State of Palestine",
          'm49_code': "275",
          'iso_a3': "PSE",
         },

         {'country': 'Russia',
          'adjectivals': 'Russian',
          'demonyms': 'Russians',
          'region_code': "150",
          'region_name': "Europe",
          'sub_region_code': "151",
          'sub_region_name': "Eastern Europe",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Russian Federation",
          'm49_code': "643",
          'iso_a3': 'RUS'},

         {'country': 'Sahrawi Arab Democratic Republic',
          'adjectivals': 'Western Saharan',
          'demonyms': 'Western Saharans',
          'region_code': "002",
          'region_name': "Africa",
          'sub_region_code': "015",
          'sub_region_name': "Northern Africa",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Western Sahara",
          'm49_code': "732",
          'iso_a3': 'ESH'
         },

         {'country': 'São Tomé and Príncipe','country_or_area': 'São Tomé and Príncipe',
          'adjectivals': 'São Toméan',
          'demonyms': 'São Toméans',
          'region_code': "002",
          'region_name': "Africa",
          'sub_region_code': "202",
          'sub_region_name': "Sub-Saharan Africa",
          'intermediate_region_code': "017",
          'intermediate_region_name': "Middle Africa",
          'country_or_area': "Sao Tome and Principe",
          'm49_code': "678",
          'iso_a3': 'STP'
         },

         {'country': 'Scotland',
          'adjectivals': 'Scottish',
          'demonyms': 'Scots',
          'region_code': "150",
          'region_name': "Europe",
          'sub_region_code': "154",
          'sub_region_name': "Northern Europe",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': 'Scotland',
          'm49_code': np.nan,
          'iso_a3': 'xSCO',
         },

         {'country': 'Syrian','country_or_area': 'Syrian',
          'adjectivals': 'Syrian',
          'demonyms': 'Syrians',
          'region_code': "142",
          'region_name': "Asia",
          'sub_region_code': "145",
          'sub_region_name': "Western Asia",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Syrian Arab Republic",
          'm49_code': "760",
          'iso_a3': 'SYR'},

         {'country': 'Taiwan','country_or_area': 'Taiwan',
          'adjectivals': 'Taiwanese',
          'demonyms': 'Taiwanese',
          'region_code': "142",
          'region_name': "Asia",
          'sub_region_code': "030",
          'sub_region_name': "Eastern Asia",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Taiwan",
          'm49_code': np.nan,
          'iso_a3': 'TWN'},

         {'country': 'Tanzania',
          'adjectivals': 'Tanzanian',
          'demonyms': 'Tanzanians',
          'region_code': "002",
          'region_name': "Africa",
          'sub_region_code': "202",
          'sub_region_name': "Sub-Saharan Africa",
          'intermediate_region_code': "014",
          'intermediate_region_name': "Eastern Africa",
          'country_or_area': "United Republic of Tanzania",
          'm49_code': "834",
          'iso_a3': 'TZA'},

         {'country': 'United Kingdom',
          'adjectivals': 'British',
          'demonyms': 'Britons',
          'region_code': "150",
          'region_name': "Europe",
          'sub_region_code': "154",
          'sub_region_name': "Northern Europe",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "United Kingdom of Great Britain and Northern Ireland",
          'm49_code': "826",
          'iso_a3': 'GBR'
         },

         {'country': 'Venezuela',
          'adjectivals': 'Venezuelan',
          'demonyms': 'Venezuelans',
          'region_code': "019",
          'region_name': "Americas",
          'sub_region_code': "419",
          'sub_region_name': "Latin America and the Caribbean",
          'intermediate_region_code': "005",
          'intermediate_region_name': "South America",
          'country_or_area': "Venezuela (Bolivarian Republic of)",
          'm49_code': "862",
          'iso_a3': 'VEN'
         },

         {'country': 'Vietnam',
          'adjectivals': 'Vietnamese',
          'demonyms': 'Vietnamese',
          'region_code': "142",
          'region_name': "Asia",
          'sub_region_code': "035",
          'sub_region_name': "South-eastern Asia",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Viet Nam",
          'm49_code': "704",
          'iso_a3': 'VNM'
         },

         {'country': 'Wales',
          'adjectivals': 'Welsh',
          'demonyms': 'Walian',
          'region_code': "150",
          'region_name': "Europe",
          'sub_region_code': "154",
          'sub_region_name': "Northern Europe",
          'intermediate_region_code': np.nan,
          'intermediate_region_name': np.nan,
          'country_or_area': "Wales",
          'm49_code': np.nan,
          'iso_a3': 'xWAL',
         },
    ]

    # Performs the replacement
    fill_values = pd.DataFrame(fill_values)
            
    nationalities = nationalities.dropna(subset=["m49_code"])
    
    nationalities = pd.concat([nationalities, fill_values]).reset_index()
        
    # Now we can select the  merged values and join them with the search result data
    nationalities["search_query"] = nationalities.adjectivals.str.lower() + " women"
    
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

