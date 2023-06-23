import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from chatclient import ChatClient
from chatserver import ChatServer


load_dotenv()
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')

app = App(token=SLACK_TOKEN)


@app.message("hello")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")


def server():
    docs = ChatServer.load_documents_from_confluence()
    ChatServer.save_documents_to_db(docs)


def client():
    cc = ChatClient()

    while (True):
        query = input(">> You >> ")
        # print("DBG:: Asking this Q: " + query)

        response = cc.chat(query)
        # print("DBG:: Answered!")
        print(">> AI >> " + response["answer"])


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
