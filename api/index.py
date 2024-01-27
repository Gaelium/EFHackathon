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
from unstructured.partition.auto import partition

os.environ["OPENAI_API_KEY"] = "sk-<your key here>"
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app = Flask(__name__)
@app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    print(file)
    #save file
    file.save(os.path.join("uploads", file.filename))

    return jsonify({"message": "File uploaded successfully"})

    

@app.route("/api/chat")
def chat():
    # get files from uploads folder
    files = os.listdir("uploads")

    # use unstructed to get the text from the files
    texts = []
    text = ""
    for file in files:
        elements = partition(UPLOAD_FOLDER + "/" + file)
        for element in elements:
            text += str(element) + " "
        texts.append(text)
    
    print(text)


    vectorstore = FAISS.from_texts(
        texts, embedding=OpenAIEmbeddings()
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

    message = chain.invoke("What is the pricing of the new large embedding model?")
    return "<p>" + message + "</p>"


@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"