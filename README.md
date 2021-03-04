# Google Images and the portrayal of women from different countries

This repository contains the source code and detailed methodology for our story about how Google Images tends to portray women from specific countries in a more sexualized way than most developed nations, especially in Latin America, Eastern Europe and Southeast Asia.

It was written by [Rodrigo Menegat](https://github.com/RodrigoMenegat) and can be read in the following languages:

- [English](#)
- [Portuguese](#)

## Data analysis

### Brief summary

In summary, the data collection and analysis for this piece happened in the following steps:

1. Searching for phrases like "german women" for 207 nationalities and territorial demonyms
2. Collecting the first 100 images and page titles that show up for each search query
3. Running the files through Google's own image analysis software to flag "racy" pictures
4. Filtering all the website titles that contain specific keywords
5. Manually reviewing both pictures and websites content to confirm the findings
6. Quantifying the reuslts

An in-depth methodological discussion can be found below.

### Methodological choices

The search results used for this piece were collected using [SerpAPI](https://serpapi.com/), a commercial service that collects data automatically from many search engines. This resource was chosen because it retrieves Google results in a computer-readable JSON format and allows a high degree of search customization.

A list of 207 countries/territories and their demonyms was compile. The demonyms were then passed, alongside the word women, as search queries for SerpAPI. The application then performed the searches form terms such as "Brazilian women" and "German women". The results were saved as JSON files.

The same searches were made in local languages for 12 select nationalities ("mulheres brasileiras", "deutsche frauen", "femmes françaises"...) in order to compare them to the English results.

After retrieving the search results, the images were downloaded and analysed by [Google Cloud Vision API](https://cloud.google.com/vision), a computer vision application that detects "racy" pictures — that is, pictures that are likely to contain elements such as "sheer clothing, strategically covered nudity, lewd or provocative pose". 

Each image was tagged as either very likely, likely, unlikely or very unlikely to contain such elements. In our analysis, we considered as "racy" the images that were marked as "very likely" or "likely".

Acknowledging that this kind of software is known to carry many biases, we did a manual review of all the pictures tagged as such to make sure that the results were reasonable. This manual review revealed that the overall trend presented in the article still holds true.

The content of the websites in which the pictures were hosted was also analysed. To do so, we first selected websites with titles that contained keywords that appear frequently in image results marked as racy. Those were terms such as "marry", "date", "hot", "bride" and "sex".

Then, these pages were also manually checked to determine if the content on display was objectifying or sexualizing in any way. This definition includes pages that write about international dating, marriage services, sexual tourism or that rank and describe women from certain nationalities based on physical features alone. 

Then, finally, the results of both datasets -- racy images and objectfying websites -- was quantified, as presented in the article.

### Caveats

#### Personalized content

Google search results are personalized (that is, each user is likely to see a different collection of images and links even when searching for the same exact words), which makes analysing them a complex task. 

Therefore, the results shown on this repository will probably differ, at least slightly, from what different users would see when doing the same search on their browsers. 

However, the overall trend is very likely to be the same. 

This was attested by comparing the results SerpAPI obtained from what people from different countries and demographics saw when doing manual searches. The results are mostly the same, despite being displayed in a different order.

The same SerpAPI data collection scripts were also run by different people, in different computers, with different location parameters. In all those sessions, at least 65% of the images retrieved were exactly the same. 

Even with this variation, the images that differed were also similar in nature to the overall trend — that is, they followed similar patterns of sexualization.

#### Computer vision bias

Computer vision software, such as Google Cloud Vision API, are know to produced skewed or biased results. This is true for this analysis as well.

The software produced a significant ammount of false positives for some specific countries, such as Namibia, where pictures of women wearing [traditional garments](https://i.ytimg.com/vi/7NKxGhgibAI/maxresdefault.jpg) that didn't cover their breasts were consistently marked as racy. 

Similar mistakes happened when the artificial intelligence analysed pictures of people in other kinds of ethnic clothing, such as pacific islander grass skirts. Other examples of misclassification include beach volleyball athletes in bikinis and feminist protesters in SlutWalk marches.  

However, as mentioned previously, a manual review of the results returned by the API revealed that the overall trend of sexualizaiton is true, despite those specific issues.

## Validation of analysis

To validate the analysis, we tried different approaches. All of them pointed to the same pattern described in the story.

### Different SerpAPI parameters

SerpAPI allows the user to make automated searches with different location parameters -- that is, informing Google's search engine that the user is located in different places throughout the world. The data was collected using this parameter as "Brazil", "Philippines", "Ukraine" and "Germany". The results were similar in all of them.


### Reproducing analysis from different locations and users

As well as collecting the data using different SerpAPI parameters, we collected it using the same exact parameters, but from different computers, users and locations. The data was collected by people based in Brazil, Germany, Greece and the United States. Again, the results were very similar.

### Comparing SerpAPI results with manual searches

In order to make sure that the results retrieved by SerpAPI were consistent with what a manual Google Search would show, we also compared the data collected with what 10 people saw when doing manual searches on their personal devices for two specific searches: "German women" and "Brazilian women". Again, the results were very similar, with slight differences in the ordering of the images displayed.

### Searches for men of different nationalities

We also did the same analysis for searches for men of different nationalities, such as "German men" and "Brazilian men". This time, the pattern was different, with a high degree of sexualization for men from highly developed countries. The results, however, didn't present nearly as many links to websites that promote blatant objetification.


## Step-by-step reproduction

The data collection and analysis is described in details on the steps below.

### English language searches

1. First, we scraped Google Image Search results using SerpAPI. using the code available on `code/1.data-collection.py`. Running this file requires SerpAPI credentials and access key, which need to be set up as a variable on the line 8 of the mentioned file. The results are saved as JSON files in the directory `output/search_results`

2. Then, we donwloaded all the image files that came up on the image search results, using the code available on `code/2.image-download.py`. This script was run a couple times to ensure that all available files were donwloaded, regardless of the eventual downtime of some websites. Those image files are saved in the directory `output/imgs/`

3. Similarly, we downloaded the HTML title tags of those websites, using the code available on `code/3.full-title-extraction.py`. The script was also run a couple times for the same reason metioned in the previos step. Those titles are saved as JSON files in the directory `output/link_contents`

4. Then, we joined the downloaded titles and image paths with their respective search entries using the code available on `code/4.aggregate-raw-data.py`. This script produces as output the file available on `output/dataset/aggregted-raw-data.csv`

5. After that, we used Google Cloud Vision API to analyse the image files using the code available on `code/5.google-vision.py`. Running this requires a Google Cloud developer account. The credentials for such account must be saved as a JSON file on the path `/credentials/portrayal-of-women-cloud-vision-credentials.json`. The results of the analysis for each image are saved on the directory `/output/vision_resulsts/`

6. Then, we merged all the data we collected into a single spreadsheet, using the script available at `code/6.aggreate-results.py`. The output is saved as a CSV file on the path `/output/dataset/complete-data.csv`

7. We then created a list of keywords to look for in the title tags of Google results, as documented in `code/7.keyword-lookup`. The keywords were defined in a iterative proccess that included terms we found anedoctally while looking at Google results, as well as using a *tf-idf* formula that identified words that were more likely to appear alongside pictures that were tagged as racy. The results are saved in a new file at `/output/dataset/complete-data-classified.csv`

8.
	1. Then, we manually checked titles that containted such keyowrds, in order to get rid of false positives like news about "hot weather" and similar exceptions. Each individual correction was saved as JSON file in the directory `/output/positives_manual_check/keywords/`. The resulting corrections are saved in `/output/dataset/compelte-data-manually-checked.csv'`. This is documented on `code/8.manual-check.ipynb`.

	2. We also manually inspected all the images that were marked as racy. The evaluation for each image is saved at `/output/positives_manual_check/imgs`. This time, however, we didn't remove images that we considered false positives, since the process would be too subjective. The goal was only to understand if there were any noticeable biases in Google's CloudVision SafeSearch software, as we mentioned on the [methodology](##methodology) section. The process is documented on `code/8.manual-check.ipynb` as well.

	3. For the same reason, we also manually checked a random sample of 352 negative images (around 2% of the total), in order to have at least an estimate of how many sexualized entries we could be missing — apparently, very few. This is also documented on `code/8.manual-check.ipynb`.

9. We then finally procceeded to do the data analysis, as documented in `code/9.data-analysis.ipynb`. All the numbers mentioned in the story come from this notebook.

10. The same process was repeated by different people, using different computers and located on a different countries. Most of the pictures were of a similar nature. The comparisons are documented at `code/10.validation.ipynb`.

### Local language searches

The same steps were followed in order to collect results for searches in local language, except for the evaluation of keywords (step 7) and the manual checking (step 8).

## Repository structure

The files in this repository are divided in the following subdirectories:

- `code`: contains the scripts used to collect, analyse and validate the story findings.
- `credentials`: should contain a JSON file with the credentials needed for using Google Cloud Vision API.
- `dataviz`: containts the Python scripts that generated basic charts which were latter edited and published with the story.
- `input`: contains a CSV file of all nationalities that were analysed, as well as their respective demonyms and adjectivals. There is also a file with the correspondence between those nationalities and the United Nations M49 standard, which divides the world in specific geographical regions.
- `local_languages`: contains the scripts and data for searches made in local languages.
- `output`: the scripts contained in the directory `code` save their outputs into this directory.
- `validation_output`: the content on this directory is similar to the one in `output`, but it was generated in other computers and with other SerpAPI/Google Cloud Vision credentials. 

### Google's position

Google didn't answer the specific questions that DW asked, but sent a statement instead.


> "Ensuring that all people and communities are able to find helpful results in Google Images is something we care about deeply and we are committed to [building inclusive experiences for everyone](https://www.blog.google/outreach-initiatives/diversity/products-work-you-no-matter-who-you-are/). Because our systems are organizing information from the open web, the ways in which images are labeled and the content available in any given country or language can affect what shows up in our results. This can lead to situations in which our results show explicit or troubling content that people may not have intended to search for, including results that reflect negative stereotypes and prejudices that exist on the web. We understand that this can be extremely upsetting and also disparately impacts women and women of color. We share the deep concern around this and are actively working towards scalable solutions for these types of issues. Over the years, we’ve made significant improvements in this area, but as the web is constantly changing, our improvements will not solve every possible query in every country or language. This is an ongoing challenge we’ll continue to work to overcome as part of our commitment to build helpful, inclusive products for all of our users around the world."
