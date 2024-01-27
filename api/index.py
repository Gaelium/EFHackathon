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
from flask import Flask, Response
from flask_cors import CORS
from threading import Thread
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth



#os.environ["SLACK_BOT_TOKEN"] = "xoxb-6543887761044-6543939519892-S3LTIe6Qmyd0a5NGuzUYC3wF"
#os.environ["SLACK_SIGNING_SECRET"] = "c5b7e8a16cc1ee9851459f6958adf327"

region = 'us-east-2'  # e.g., 'us-west-1'
service = 'es'
awsauth = AWS4Auth(os.environ["AWS_ACCESS_KEY_ID"], os.environ["AWS_SECRET_ACCESS_KEY"], region, service)

# OpenSearch Service configuration
host = 'vpc-efhackathon-5rob5xakxqvslsdyqhoz5s5dbq.us-east-2.es.amazonaws.com'  # e.g., 'search-mydomain.us-west-1.es.amazonaws.com'
index_name = 'text_documents'
type_name = '_doc'

#Elasticsearch instance
es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

LOCAL_DOWNLOAD_PATH = 'downloads'
os.makedirs(LOCAL_DOWNLOAD_PATH, exist_ok=True)

BUCKET_NAME = 'defaultefhackathon'
s3_client = boto3.client('s3')

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

@app.route("/api/upload", methods=["POST"])
def upload():
    print("uploading file")
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

    message = chain.invoke(query)
    return jsonify({"message": message})
