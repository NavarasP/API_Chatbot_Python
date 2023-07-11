import os
import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# from langchain.document_loaders import WebBaseLoader
# from langchain.document_loaders import TextLoader
# from langchain.document_loaders import DirectoryLoader
# from langchain.indexes import VectorstoreIndexCreator
# from langchain. llms import OpenAI

# from langchain.text_splitter import CharacterTextSplitter
# import pickle
# import faiss
# from langchain.vectorstores import FAISS
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.chains import RetrievalQAWithSourcesChain
# from langchain.chains.question_answering import load_qa_chain
# from langchain import OpenAI

# from langchain.chat_models import ChatopenAI



# query = sys.argv[1]
# loader = TextLoader( 'data.txt' )
# loader = DirectoryLoader('./data')
# data = loader.load()

# text_splitter = CharacterTextSplitter(separator='\n', 
#                                       chunk_size=1000, 
#                                       chunk_overlap=200)
# docs = text_splitter.split_documents(data)

# embeddings = OpenAIEmbeddings()

# with open("faiss_store_openai.pkl", "rb") as f:
#     VectorStore = pickle.load(f)

# llm=OpenAI(temperature=0, model_name='')
# chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=VectorStore.as_retriever())
# chain({"question": "How big is stableLM?"}, return_only_outputs=True)





# index = VectorstoreIndexCreator().from_loaders([loader])

# print(index.query(query))







# from langchain.document_loaders import WebBaseLoader
# from langchain.indexes import VectorstoreIndexCreator



# loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
# index = VectorstoreIndexCreator().from_loaders([loader])
# question = "What is Task Decomposition?"
# index.query(question)








from flask import Flask, request, jsonify
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

import constants

app = Flask(__name__)
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

@app.route('/api/chat', methods=['POST'])
def chat():
    query = request.json['query']

    if query.lower() in ['quit', 'q', 'exit']:
        return jsonify({'answer': 'Goodbye!'})

    result = chain({"question": query, "chat_history": chat_history})
    answer = result['answer']

    chat_history.append((query, answer))
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run()
