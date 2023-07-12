import os
import time
import constants
# import sys

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
# from langchain.llms import OpenAI
from langchain.vectorstores import Chroma




app = Flask(__name__)
CORS(app)
os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

if PERSIST and os.path.exists("persist"):
    print("Reusing index...\n")
    vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    loader = DirectoryLoader("data/")
    if PERSIST:
        index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
    else:
        index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []

@app.route('/', methods=['GET'])
def get():
    return jsonify('Hello World! Dont Try')

MAX_RETRY_COUNT = 3

@app.route('/api/chat', methods=['POST'])
def chat():
    query = request.json['query']
    print("Received query:", query)

    if query.lower() in ['quit', 'q', 'exit']:
        return jsonify({'answer': 'Goodbye!'})

    retry_count = 0
    while retry_count < MAX_RETRY_COUNT:
        try:
            result = chain({"question": query, "chat_history": chat_history})
            answer = result['answer']

            chat_history.append((query, answer))
            return jsonify({'answer': answer})
        except openai.error.RateLimitError as e:
            print("Rate limit reached. Retrying in 20 seconds...")
            time.sleep(20)
            retry_count += 1
            continue
        except Exception as e:
            print("An error occurred:", str(e))
            return jsonify({'answer': 'An error occurred. Please try again later.'})

    return jsonify({'answer': 'Rate limit exceeded. Please try again later.'})

if __name__ == '__main__':
    app.run()