import os, sys, re
import requests
import pickle
from bs4 import BeautifulSoup as bs
from article import *

def remove_attrs(soup, whitelist=tuple()):
    for tag in soup.findAll(True):
        for attr in [attr for attr in tag.attrs if attr not in whitelist]:
            del tag[attr]
    return soup

def get_html(url):
    res = requests.get(url)
    if not res: return False
    html = res.text
    return html

def parse_html(html):
    soup = bs(html, "html.parser")
    # decompose script and style
    for s in soup(["script", "style", "code"]):
        s.decompose()
    if soup.find("div", {"style":"overflow-x: auto;"}) is not None:
        tmp = soup.findAll("div", {"style":"overflow-x: auto;"})
        for t in tmp:
            t.decompose()
    # remove_attrs(soup, ("style",))
    text = soup.get_text()
    
    # print(text)
    stripped = []
    for line in text.splitlines():
        tmp = line.strip()
        if tmp:
            tmp = re.sub("\$.+?\$", "", tmp)
            stripped.append(tmp)
    # lines = [line.strip() for line in text.splitlines()]
    return stripped

def get_article_titles():
    titles = os.listdir("/Users/seiichi/Desktop/repositories/web/blog/content/post/")
    titles_new = []
    for title in titles:
        if not title.endswith(".md"):
            continue
        titles_new.append(title)
    return titles_new

def main():
    articles = []
    titles = get_article_titles()
    for t in titles:
        t = t.replace(".md", "")
        html = get_html("https://seiichiinoue.github.io/post/{}".format(t))
        if not html: continue
        text = parse_html(html)
        text = text[5:-4]
        # create article abject
        article = Article()
        article.set_name(t)
        article.set_title(text[0])
        article.set_raw_text(text)
        articles.append(article)
        # write to file par document
        with open("./data/raw/{}.txt".format(t),"w") as f:
            for line in text:
                f.write(line)
                f.write('\n')
    with open("./data/objects/articles.pickle", "wb") as f:
        pickle.dump(articles, f)

if __name__ == '__main__':
    # html = get_html("https://seiichiinoue.github.io/post/tobit/")
    # text = parse_html(html)
    # print(text)
    main()
