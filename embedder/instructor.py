from langchain.vectorstores import FAISS
import pickle
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import markdown

class Instructor:

    def __init__(self, store_name, path):
        self.store_name = store_name
        self.path = path
        self.instructor_embeddings = HuggingFaceInstructEmbeddings(
            model_name="hkunlp/instructor-xl",
            model_kwargs={"device": "cuda"}
        )

    def store_embeddings(self, docs):
        vector_store = FAISS.from_documents(docs, self.instructor_embeddings)




    def load_embeddings(self, store_name, path):
        with open(f"{path}/faiss_{store_name}.pkl", "rb") as f:
            VectorStore = pickle.load(f)
        return VectorStore
