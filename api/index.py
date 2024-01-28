from flask import Flask, request, session, jsonify, Response
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
from flask_cors import CORS
from threading import Thread
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

region = 'us-east-2'  # e.g., 'us-west-1'
service = 'es'
awsauth = AWS4Auth(os.environ["AWS_ACCESS_KEY_ID"], os.environ["AWS_SECRET_ACCESS_KEY"], region, service)

# ... [previous code] ...

# Corrected OpenSearch Service configuration
host = 'search-hackathon-qnnu5nwwyydblg2pnmb5ej2po4.us-east-2.es.amazonaws.com'
index_name = 'text_documents'
type_name = '_doc'
master_username = 'ccappy'  # Replace with your master username
master_password = 'Pecky123!'
# Corrected Elasticsearch instance setup
es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=(master_username, master_password),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

# ... [rest of your code] ...

LOCAL_DOWNLOAD_PATH = 'downloads'
os.makedirs(LOCAL_DOWNLOAD_PATH, exist_ok=True)

BUCKET_NAME = 'defaultefhackathon'
s3_client = boto3.client('s3')

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


import base64

def index_file_content_to_opensearch(file_key):
    file_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_content = file_obj['Body'].read()

    # Encode the binary content in base64
    encoded_content = base64.b64encode(file_content).decode('utf-8')

    document = {"content": encoded_content}
    es.index(index=index_name, doc_type=type_name, body=document)


@app.route("/api/upload", methods=["POST"])
def upload():
    print("uploading file")
    file = request.files["file"]
    if file:
        file_path_in_s3 = f"{file.filename}"
        
        # Upload file to S3
        s3_client.upload_fileobj(file, BUCKET_NAME, file_path_in_s3)


        return jsonify({"message": "File uploaded and indexed successfully"})

    return jsonify({"message": "No file found"})

    

def list_files_in_bucket(bucket_name):
    """List files in an S3 bucket."""
    files = s3_client.list_objects_v2(Bucket=bucket_name)
    return [file['Key'] for file in files.get('Contents', [])]

def download_file(bucket_name, s3_file_key, local_path):
    """Download a file from S3 to a local path."""
    s3_client.download_file(bucket_name, s3_file_key, local_path)

def search_documents(query):
    """Perform a full-text search in the OpenSearch index."""
    search_body = {
        "query": {
            "match": {
                "text": query
            }
        }
    }
    response = es.search(index=index_name, body=search_body)
    return response['hits']['hits']

def process_search_query(query):
    search_results = search_documents(query)

    relevant_documents = []
    for result in search_results:
        document_id = result['_id']
        document_text = result['_source']['text']
        relevant_documents.append((document_id, document_text))

    # Now you have a list of relevant documents (document_id, document_text)
    # You can further process these documents or send them to your RAG chain

    return relevant_documents

@app.route("/api/chat", methods=["POST"])
def chat(): 

    # get files from uploads folder
    #the query is just the body of the request
    data = request.get_json()

    # Extract the 'message' field
    query = data.get('message', '')

    files = list_files_in_bucket(BUCKET_NAME)
    print(files)
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

    print(texts)

    vectorstore = FAISS.from_texts(
        texts, embedding=OpenAIEmbeddings()
    )
    retriever = vectorstore.as_retriever()

    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    #use
    model = ChatOpenAI(model="gpt-4-1106-preview")

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    message = chain.invoke(query)
    return jsonify({"message": message})



@app.route("/api/slack")
def slack():
    file_name = "channel_messages.txt"
    with open(file_name, "w") as f:
        slack_token = "xoxb-6543887761044-6541467149635-cTWCHuzrDyaYNb6bu8CYPtp1"  # Use your actual token
        os.environ["SLACK_BOT_TOKEN"] = slack_token
        client = WebClient(token=slack_token)
        logger = logging.getLogger(__name__)

        try:
            channel_lists = client.conversations_list()
            for channel in channel_lists["channels"]:
                result = client.conversations_history(channel=channel["id"])
                conversation_history = result["messages"]
                for message in conversation_history:
                    if not message["text"].endswith("has joined the channel"):
                        f.write(message["text"])
                        f.write("\n")
        except SlackApiError as e:
            logger.error(f"Error creating conversation: {e}")
            return jsonify({"message": f"Error: {e}"})

    # Upload file to S3
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, BUCKET_NAME, file_name)
        return jsonify({"message": "File uploaded successfully to S3"})
    except Exception as e:
        logger.error(f"Error uploading to S3: {e}")
        return jsonify({"message": f"Error uploading to S3: {e}"})
