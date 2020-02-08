import os, sys, pickle
import numpy as np
import MeCab, gensim
from collections import defaultdict

# to run this script, you must have done
#   - prepare document data
#   - prepare wakatied data
#   - locate data at `./data/wakati`

def calc_freq_of_all_words(word_list):
    frequency_of_words = defaultdict(int)
    for word in word_list:
        frequency_of_words[word] += 1
    return frequency_of_words

def create_dataset(documents, ignore_word=0):
    word_list = []
    for sentences in documents:
        for sentence in sentences:
            for word in sentence.strip().split():
                word_list.append(word)
    freq_dic = calc_freq_of_all_words(word_list)
    doc_new = []
    for sentences in documents:
        doc = []
        for sentence in sentences:
            for word in sentence.strip().split():
                if freq_dic[word] > ignore_word:
                    doc.append(word)
        doc_new.append(doc)
    dictionary = gensim.corpora.Dictionary(doc_new)
    dictionary.filter_extremes(no_below=3, no_above=0.3)
    print("vocab size: {}".format(len(dictionary)))
    corpus = []
    for document in doc_new:
        bow = dictionary.doc2bow(document)
        corpus.append(bow)
    return corpus, dictionary

def train_model(n_topic=4):
    documents = []
    # article_list = os.listdir("./data/wakati/")
    with open("./data/objects/articles.pickle", "rb") as f:
        articles = pickle.load(f)
    id2doc = dict()
    id2title = dict()
    for i, article in enumerate(articles):
        id2doc[i] = article.name
        id2title[i] = article.title
    # print(id2doc)
    for article in articles:
        documents.append(article.processed_text)
    corpus, dictionary = create_dataset(documents)
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=n_topic, random_state=0)
    print("pplx: {}".format(np.exp2(-lda_model.log_perplexity(corpus))))
    
    lda_model.save("./model/lda.model")
    with open("./model/corpus.pickle", "wb") as f:
        pickle.dump(corpus, f)
    with open("./model/id2doc.pickle", "wb") as f:
        pickle.dump(id2doc, f)
    with open("./model/id2title.pickle", "wb") as f:
        pickle.dump(id2title, f)
    with open("./model/dictionary.pickle", "wb") as f:
        pickle.dump(dictionary, f)

def allocate_topic_to_documents(model_path="./model/lda.model"):
    model = gensim.models.ldamodel.LdaModel.load(model_path)
    with open("./model/corpus.pickle", "rb") as f:
        corpus = pickle.load(f)
    with open("./model/id2doc.pickle", "rb") as f:
        id2doc = pickle.load(f)
    with open("./model/dictionary.pickle", "rb") as f:
        dictionary = pickle.load(f)
    # print(model.num_topics)
    # print(model.get_document_topics(corpus[0]))
    topic = [0] * len(corpus)
    for i in range(len(corpus)):
        res = model.get_document_topics(corpus[i])
        max_t = 0
        max_p = 0
        for t, p in res:
            if p > max_p:
                max_p = p
                max_t = t
        topic[i] = max_t
        print(id2doc[i], topic[i])
        # print(res)
    #with open("./model/topic.pickle", "wb") as f:
        #pickle.dump(topic, f)
    return topic

def get_topic():
    with open("./model/dictionary.pickle", "rb") as f:
        dictionary = pickle.load(f)
    model = gensim.models.ldamodel.LdaModel.load("./model/lda.model")
    for i in range(model.num_topics):
        topic = model.get_topic_terms(i)
        print("topic {}".format(i))
        for id, p in topic:
            print(dictionary[id], p)

# def find_similar_docs(doc_id):

if __name__ == '__main__':
    # for i in range(2, 10):
        # print("num_topic:", i)
        # train_model(i)
    train_model()
    # get_topic()
    # allocate_topic_to_documents()

