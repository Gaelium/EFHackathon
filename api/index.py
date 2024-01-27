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
import boto3
from unstructured.partition.auto import partition

os.environ["OPENAI_API_KEY"] = ""
os.environ["AWS_ACCESS_KEY_ID"] = ""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""
LOCAL_DOWNLOAD_PATH = 'downloads'
os.makedirs(LOCAL_DOWNLOAD_PATH, exist_ok=True)

BUCKET_NAME = 'defaultefhackathon'
s3_client = boto3.client('s3')

app = Flask(__name__)
@app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file:
        # S3 path where file will be uploaded
        file_path_in_s3 = f"{file.filename}"

        # Upload file to S3
        s3_client.upload_fileobj(
            file,
            BUCKET_NAME,
            file_path_in_s3
        )
        return jsonify({"message": "File uploaded successfully to S3"})

    return jsonify({"message": "No file found"})

    

def list_files_in_bucket(bucket_name):
    """List files in an S3 bucket."""
    files = s3_client.list_objects_v2(Bucket=bucket_name)
    return [file['Key'] for file in files.get('Contents', [])]

def download_file(bucket_name, s3_file_key, local_path):
    """Download a file from S3 to a local path."""
    s3_client.download_file(bucket_name, s3_file_key, local_path)

@app.route("/api/chat")
def chat():
    # get files from uploads folder
    files = list_files_in_bucket(BUCKET_NAME)
    texts = []
    text = ""
    # Process each file
    for s3_file_key in files:
        local_file_path = os.path.join(LOCAL_DOWNLOAD_PATH, os.path.basename(s3_file_key))
        download_file(BUCKET_NAME, s3_file_key, local_file_path)

    # use unstructed to get the text from the files
    files = os.listdir(LOCAL_DOWNLOAD_PATH)
    for file in files:
        elements = partition(LOCAL_DOWNLOAD_PATH + "/" + file)
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