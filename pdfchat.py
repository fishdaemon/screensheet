from Class import webuiLLM

import streamlit as st
from PyPDF2 import PdfReader

import langchain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import LlamaCpp
from langchain.vectorstores import Qdrant
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

langchain.verbose = False


def main():
    # Callback just to stream output to stdout, can be removed
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = webuiLLM()

    # Load question answering chain
    chain = load_qa_chain(llm, chain_type="stuff")

    if "Helpful Answer:" in chain.llm_chain.prompt.template:
        chain.llm_chain.prompt.template = (
            f"### Human:{chain.llm_chain.prompt.template}".replace(
                "Helpful Answer:", "\n### Assistant:"
            )
        )

    # Page setup
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF 💬")
    pdf = st.file_uploader("Upload a PDF", type=["pdf"])

    if pdf:
        pdf_reader = PdfReader(pdf)

        # Collect text from pdf
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Split the text into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
        )
        chunks = text_splitter.split_text(text)

        #embeddings = SentenceTransformerEmbeddings(model_name='hku-nlp/instructor-large')
        embeddings = SentenceTransformerEmbeddings(model_name="flax-sentence-embeddings/all_datasets_v4_MiniLM-L6")

        # Create in-memory Qdrant instance
        knowledge_base = Qdrant.from_texts(
            chunks,
            embeddings,
            location=":memory:",
            collection_name="doc_chunks",
        )

        user_question = st.text_input("Ask a question about your PDF:")

        if user_question:
            docs = knowledge_base.similarity_search(user_question, k=4)

            # Calculating prompt (takes time and can optionally be removed)
            prompt_len = chain.prompt_length(docs=docs, question=user_question)
            st.write(f"Prompt len: {prompt_len}")
            # if prompt_len > llm.n_ctx:
            #     st.write(
            #         "Prompt length is more than n_ctx. This will likely fail. Increase model's context, reduce chunk's \
            #             sizes or question length, or retrieve less number of docs."
            #     )

            # Grab and print response
            response = chain.run(input_documents=docs, question=user_question)
            st.write(response)


if __name__ == "__main__":
    main()