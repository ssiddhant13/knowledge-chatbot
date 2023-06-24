import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import ConfluenceLoader

DATABASE_FOLDER = 'embedding_db'
CONFLUENCE_SPACE = "CMEKB"
CONFLUENCE_USER = "yash.kulkarni"


class ChatServer:
    def load_documents_from_confluence():
        loader = ConfluenceLoader(
            url="https://confluence.internal.salesforce.com", 
            username=CONFLUENCE_USER, 
            api_key=os.getenv("CONFLUENCE_API_KEY"), 
            confluence_kwargs={"verify_ssl": False}
        )
        documents = loader.load(space_key= CONFLUENCE_SPACE, include_attachments=True, limit=50)
        return documents


    def save_documents_to_db(documents): 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        embedding = OpenAIEmbeddings()
        vectordb = Chroma.from_documents(documents=texts, 
                                        embedding=embedding,
                                        persist_directory=DATABASE_FOLDER)
        vectordb.persist()
