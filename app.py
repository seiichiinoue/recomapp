import sys, os
import flask
import numpy as np
sys.path.append("./cstm/") # to import pre-trained cstm model
import pycstm
# initialize our Flask application and pre-trained model
app = flask.Flask(__name__)

def find_sim_docs(tar):
    tar = tar
    cstm = pycstm.cstm("./cstm/model/cstm.model")
    docs = cstm.get_docs_similar_to_file(tar, 10)
    sim_docs = []
    for meta in docs:
        doc_id, doc, vector, cosine = meta
        sim_docs.append(doc)
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
