from flask import Flask, request, session, jsonify
from operator import itemgetter
import requests
import json
import os
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

app = Flask(__name__)
#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
@app.route("/api/upload", methods=["POST"])
def upload():
    files = request.files.getlist('files')

    #handle no file part
    if len(files) == 0:
        return "No file part"
    

@app.route("/api/chat")
def chat():
    vectorstore = FAISS.from_texts(
        ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
    )
    retriever = vectorstore.as_retriever()

    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    model = ChatOpenAI()

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    message = chain.invoke("where did harrison work?")
    return "<p>" + message + "</p>"


@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"