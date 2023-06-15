from flask import Flask, request
from embedder import Instructor


from langchain.text_splitter import NLTKTextSplitter
import nltk
import json


nltk.download("punkt")
app = Flask(__name__)

STORAGE_PATH = "db"


@app.route('/api/embedding', methods=['POST'])
def embedding():
    name = request.form.get('name')
    # i = Instructor(store_name=name, path=STORAGE_PATH)

    # markdown_text = UnstructuredMarkdownLoader(request.get_data().decode('utf-8'))
    markdown_text = request.form.get("markdown")
    #print(markdown_text)
    text = NLTKTextSplitter(chunk_size=1000, chunk_overlap=200)
    split = text.split_text(markdown_text)
    #print(split)
    return split
    # return jsonify(dict(result=markdown_text))

    #    splitter = NLTKTextSplitter(chunk_size=1000)

    # text = markdown_text.load_and_split(MarkdownTextSplitter())



if __name__ == '__main__':
    app.run(debug=False, port=1337)
