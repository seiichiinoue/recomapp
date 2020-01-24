import sys, os
import flask
import numpy as np
import pickle
import gensim
# initialize our Flask application and pre-trained model
app = flask.Flask(__name__)

def find_sim_docs(tar, model_path="./model/lda.model"):
    # load objects to infer similar documents
    with open("./model/corpus.pickle", "rb") as f:
        corpus = pickle.load(f)
    with open("./model/id2doc.pickle", "rb") as f:
        id2doc = pickle.load(f)
    doc2id = {doc:id for id, doc in id2doc.items()}
    print(doc2id)
    with open("./model/dictionary.pickle", "rb") as f:
        dictionary = pickle.load(f)
    model = gensim.models.ldamodel.LdaModel.load(model_path)
    target_document = tar
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
    # find similar documents from topic list
    target_topic = topics[doc2id[target_document]]
    sim_docs = []
    for doc_id, topic in enumerate(topics):
        if topic == target_topic and doc_id != doc2id[target_document]:
            sim_docs.append(id2doc[doc_id])
    return sim_docs

@app.route("/infer", methods=["POST"])
def infer():
    response = {
        "success": False,
        "Content-Type": "application/json"
    }
    # ensure an feature was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.get_json().get("filename"):
            # read feature from json
            filename = flask.request.get_json().get("filename")

            # classify the input feature
            response["prediction"] = find_sim_docs(filename)

            # indicate that the request was a success
            response["success"] = True
    # return the data dictionary as a JSON response
    return flask.jsonify(response)


if __name__ == "__main__":
    print(" * starting server...")
    app.run()
