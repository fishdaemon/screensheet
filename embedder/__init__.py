from .instructor import Instructor
#
# from langchain.embeddings import HuggingFaceInstructEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.llms import OpenAI
# from langchain.chains import RetrievalQA
# from langchain.document_loaders import PyPDFLoader, markdown
# from langchain.document_loaders import DirectoryLoader
# import pickle
# import faiss
# from langchain.vectorstores import FAISS
#
#
# def store_embeddings(docs, embeddings, store_name, path):
#     vectorStore = FAISS.from_documents(docs, embeddings)
#
#     with open(f"{path}/faiss_{store_name}.pkl", "wb") as f:
#         pickle.dump(vectorStore, f)
#
#
# def load_embeddings(store_name, path):
#     with open(f"{path}/faiss_{store_name}.pkl", "rb") as f:
#         VectorStore = pickle.load(f)
#     return VectorStore
#
# loader = DirectoryLoader(f'{root_dir}/Documents/', glob="./*.pdf", loader_cls=PyPDFLoader)
# documents = loader.load()
#
# instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl",
#                                                       model_kwargs={"device": "cuda"})
#
# Embedding_store_path = f"{root_dir}/Embedding_store"
#
# # store_embeddings(texts,
# #                  instructor_embeddings,
# #                  sotre_name='instructEmbeddings',
# #                  path=Embedding_store_path)
#
# # db_instructEmbedd = load_embeddings(sotre_name='instructEmbeddings',
# #                                     path=Embedding_store_path)
#
# db_instructEmbedd = FAISS.from_documents(texts, instructor_embeddings)
#
# retriever = db_instructEmbedd.as_retriever(search_kwargs={"k": 3})
#
# retriever.search_type
#
# retriever.search_kwargs
#
# docs = retriever.get_relevant_documents("Who are the authors of GPT4All report?")