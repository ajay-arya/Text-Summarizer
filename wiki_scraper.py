import bs4
import requests
import re

response = requests.get("https://en.wikipedia.org/wiki/International_Space_Station")
# response = requests.get(wiki_url)
if response is not None:
    html = bs4.BeautifulSoup(response.text, 'html.parser')
#     title = html.select("#firstHeading")[0].text
    paragraphs = html.select("p")
    for para in paragraphs:
        print (para.text)
    # just grab the text up to contents as stated in question
    intro = '\n'.join([ para.text for para in paragraphs[0:5]])
    
    print(intro)


def wiki_scrape(wiki_url):
    # response = requests.get("https://en.wikipedia.org/wiki/International_Space_Station")
    response = requests.get(wiki_url)
    intro = ''
    if response is not None:
        html = bs4.BeautifulSoup(response.text, 'html.parser')

    #     title = html.select("#firstHeading")[0].text
        paragraphs = html.select("p")
        for para in paragraphs:
            # print (para.text)
            intro += para.text

        # just grab the text up to contents as stated in question
        # intro = '\n'.join([ para.text for para in paragraphs[0:5]])
        x = re.sub(r"\[[0-9+]]", " ", intro)
        print(intro)
        return intro