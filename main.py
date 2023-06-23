from dotenv import load_dotenv
from chatclient import ChatClient
from chatserver import ChatServer

def main():
    load_dotenv()


def server():
    docs = ChatServer.load_documents_from_confluence()
    ChatServer.save_documents_to_db(docs)

def client():
    cc = ChatClient()

    while(True):
        query = input(">> You >> ")
        # print("DBG:: Asking this Q: " + query)
        
        response = cc.chat(query)
        # print("DBG:: Answered!")
        print(">> AI >> " + response["answer"])
