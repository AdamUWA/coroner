
import os
import pandas as pd
import streamlit as st
from pathlib import Path

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore

from qanda import QandA
from models import get_available_models


available_models = get_available_models()
available_models.remove('mxbai-embed-large')
available_models = [None] + available_models

DATA_DIR = './jsondata'

if os.path.exists(DATA_DIR):
    file_names = os.listdir(DATA_DIR)
else:
    print("No data. Exiting...") # terminal
    st.subheader("No data.")     # app
    exit()

documents = [None] + [os.path.splitext(name)[0] for name in file_names]


st.title("Welcome to Coroner App")

st.divider()
st.button("Refresh", on_click=st.cache_resource.clear())

st.subheader("Choose your model")
chosen_model = st.selectbox("", available_models)

st.subheader("Choose your document")
chosen_document = st.selectbox("", documents)


if chosen_document != None:

    FILE_PATH = Path('jsondata/' + chosen_document + '.jsonl')

    if os.path.exists(FILE_PATH):
        st.write(FILE_PATH)
    else:
        st.write("Error: no data")

    GEN_MODEL = chosen_model
    EMBED_MODEL = "mxbai-embed-large"
    VDB = InMemoryVectorStore
    TOP_K = 3

    PROMPT = ChatPromptTemplate.from_template(
        """Context information is below.
        \n---------------------\n
        {context}
        \n---------------------\n
        Given the context information and not prior knowledge, answer the query.\n
        Query: {input}\n
        Answer:\n""",
    )

    @st.cache_resource
    def qanda():
        return QandA(gen_model=GEN_MODEL,
                     embed_model=EMBED_MODEL, 
                     vdb=VDB,
                     file_path=FILE_PATH,
                     top_k=TOP_K,
                     prompt=PROMPT)

    qanda = qanda()

    st.text("")
    st.text("")
    st.subheader("Ask a question")
    question = st.text_area("", None)

    if question != None:
        answer, sources = qanda.ask(str(question), verbose=True)
        st.write(answer)
        st.write(sources)

