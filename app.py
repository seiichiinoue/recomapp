import sys, os, random
import flask
from flask_cors import CORS
import numpy as np
import pickle
import gensim
# initialize our Flask application and pre-trained model
app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config["JSON_SORT_KEYS"] = False
CORS(app)   # for cross-origin resource sharing

def find_sim_docs(tar, model_path="./model/lda.model"):
    # load objects to infer similar documents
    with open("./model/corpus.pickle", "rb") as f:
        corpus = pickle.load(f)
    with open("./model/id2doc.pickle", "rb") as f:
        id2doc = pickle.load(f)
    with open("./model/id2title.pickle", "rb") as f:
        id2title = pickle.load(f)
    doc2id = {doc:id for id, doc in id2doc.items()}
    title2id = {title:id for id, title in id2title.items()}
    # print(title2id)
    with open("./model/dictionary.pickle", "rb") as f:
        dictionary = pickle.load(f)
    model = gensim.models.ldamodel.LdaModel.load(model_path)
    target_document = tar
    # exception hundling: DocumentNotFoundError
    if target_document not in doc2id.keys():
        return [], []
    # allocate topic to documents
    topics = [0] * len(corpus)
    for i in range(len(corpus)):
        res = model.get_document_topics(corpus[i])
        topic_index, topic_prob = 0, 0
        for t, p in res:
            if p > topic_prob:
                topic_index = t
                topic_prob = p
        topics[i] = topic_index
    # print(topics)
    # find similar documents from topic list
    target_topic = topics[doc2id[target_document]]
    sim_docs_name, sim_docs_title = [], []
    for doc_id, topic in enumerate(topics):
        if topic == target_topic and doc_id != doc2id[target_document]:
            sim_docs_name.append(id2doc[doc_id])
            sim_docs_title.append(id2title[doc_id])
    return sim_docs_name, sim_docs_title

def shuffle(a, b):
    tmp = [[i, j] for i, j in zip(a, b)]
    random.shuffle(tmp)
    anew, bnew = [], []
    for i, j in tmp:
        anew.append(i)
        bnew.append(j)
    return anew, bnew

@app.route("/infer", methods=["POST","GET"])
def infer():
    response = {
        "success": False,
        "Content-Type": "application/json"
    }
    # ensure an feature was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.get_json().get("name"):
            # read feature from json
            name = flask.request.get_json().get("name")
            # predict similar documents of requested document
            names, titles = find_sim_docs(name)
            response["similar_doc_name"] = names
            response["similar_doc_title"] = titles
            # indicate that the request was a success
            response["success"] = (names != [] and titles != [])

    elif flask.request.method == "GET":
        if flask.request.args.get("name"):
            name = flask.request.args.get("name")
            names, titles = find_sim_docs(name)
            names, titles = shuffle(names, titles)
            response["similar_doc_name"] = names
            response["similar_doc_title"] = titles
            response["success"] = (names != [] and titles != [])

    # return the data dictionary as a JSON response
    return flask.jsonify(response)


if __name__ == "__main__":
    print(" * starting server...")
    app.run()
