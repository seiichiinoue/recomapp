import os, sys, re
import requests
from bs4 import BeautifulSoup as bs

def remove_attrs(soup, whitelist=tuple()):
    for tag in soup.findAll(True):
        for attr in [attr for attr in tag.attrs if attr not in whitelist]:
            del tag[attr]
    return soup

def get_html(url):
    html = requests.get(url).text
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
    return titles

def main():
    titles = get_article_titles()
    for t in titles:
        t = t.replace(".md", "")
        html = get_html("https://seiichiinoue.github.io/post/{}".format(t))
        text = parse_html(html)
        text = text[6:-4]
        with open("./data/{}.txt".format(t),"w") as f:
            for line in text:
                f.write(line)
                f.write('\n')

if __name__ == '__main__':
    # html = get_html("https://seiichiinoue.github.io/post/tobit/")
    # text = parse_html(html)
    # print(text)
    main()
