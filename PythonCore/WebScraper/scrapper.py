import requests
import os
from bs4 import BeautifulSoup as bs
import string


def get_article(url):
    art = bs(requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'}).content, "html.parser")
    art_text = art.find("div", {"class" : "c-article-body u-clearfix"})
    return art_text.get_text().strip()


def to_filename(str):
    fixed = str.replace(" ", "_").strip()
    for letter in string.punctuation:
        if "_" == letter:
            continue
        else:
            fixed = fixed.replace(letter, "")
    return fixed


url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
base_url = "https://www.nature.com"
LAST_PAGE = 182
num_pages = int(input("Enter the number pages:"))
article_type = input("Enter the type of article:").lower()
for current_page in range(1, num_pages + 1):
    current_folder = f"Page_{current_page}"
    try:
        os.mkdir(current_folder)
    except FileExistsError:
        print(f"Folder {current_folder} Already Exists")
    current_page_url = url + f"&page={current_page}"
    r = requests.get(current_page_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if not r:
        print("The URL returned " + str(r.status_code))
        exit()
    soup = bs(r.content, 'html.parser')
    articles = soup.find_all("article")
    saved_articles = {}
    for article in articles:
        article_soup = bs(str(article), "html.parser")
        if article_soup.find("span", "c-meta__type").text.lower() == article_type:
            # print(article_soup.contents)
            try:
                title = to_filename(article_soup.find("h3").text.strip()) + ".txt"
                url = base_url + article_soup.find("a").get("href")
            except AttributeError:
                continue
            saved_articles[title] = url
    print("Saved articles:\t" + str(saved_articles))
    for title, url in saved_articles.items():
        with open(current_folder + "/" + title, "w", encoding="utf-8") as file:
            text = get_article(url)
            file.write(text)
