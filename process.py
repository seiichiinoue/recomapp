import argparse, os, unicodedata
import MeCab

class Text(object):
    def __init__(self, text):
        self.wakati = MeCab.Tagger('-Owakati')
        self.chasen = MeCab.Tagger('-Ochasen')
        self.text = text
        for i in range(len(self.text)):
            self.text[i] = self.text[i].replace("\n", "")

    def _is_japanese(self, text):
        for c in ['CJK UNIFIED', 'HIRAGANA', 'KATAKANA']:
            if c in unicodedata.name(text):
                return True
        return False

    def _wakati(self, path):
        #if self._is_japanese(self.text[0][0]):
        processed = self._wakati_ja(path)
        #else:
        #self._wakati_en(path)
        return processed 

    def _wakati_ja(self, path):
        wakatied = []
        for i in range(len(self.text)):
            new_t = self.wakati.parse(self.text[i]).strip("\n")
            wakatied.append(new_t)
        with open(path, "w") as f:
            for t in wakatied:
                f.write(t+'\n')
        return wakatied
    
    def _wakati_en(self, path):
        wakatied = []
        for i in range(len(self.text)):
            new_t = self.text[i].split(" ").strip("\n")
            wakatied.append(new_t)
        with open(path, "w") as f:
            for t in wakatied:
                f.write(t+'\n')
        return None

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='this script for text processing.')
    # parser.add_argument('--tar_path', help='directory located raw file')
    # parser.add_argument('--save_path', help='directory save processed text')
    # args = parser.parse_args()
    # filelist = os.listdir(args.tar_path)
    # for file in filelist:
        # if file.endswith(".txt"):
            # t = Text(args.tar_path+file)
            # t._wakati(args.save_path+file)
    import pickle
    with open("./data/objects/articles.pickle", "rb") as f:
        articles = pickle.load(f)
    articles_new = []
    for article in articles:
        t = Text(article.raw_text)
        processed = t._wakati("./data/wakati/{}.txt".format(article.name))
        article_new = article
        article_new.set_processed_text(processed)
        articles_new.append(article_new)
    
    with open("./data/objects/articles.pickle", "wb") as f:
        pickle.dump(articles_new, f)
