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
thread_to_chat_client = {}


@app.message()
def reply_to_any_message(message, say):
    logger.debug(message)

    if not message.get("thread_ts"):
        ts = message.get("ts")
        thread_to_chat_client[ts] = ChatClient()

    thread_ts = message.get("thread_ts", None) or message["ts"]
    say(":waiting-resp:", thread_ts=thread_ts)

    chat_client = thread_to_chat_client.get(thread_ts)
    if not chat_client:
        say("Sorry, this chat thread has been closed. Please initiate a new chat thread.", thread_ts=thread_ts)
        return
    
    chat_reply = generate_reply(message.get("text"), chat_client)
    say(chat_reply, thread_ts=thread_ts)


def generate_reply(query_text, chat_client):
    chat_response = chat_client.chat(query_text)
    logger.debug(chat_response)
    source_text = extract_sources(chat_response)

    return chat_response["answer"] + source_text


def extract_sources(chat_response):
    source_text = "\n\n*Sources*\n"
    for source_doc in chat_response["source_documents"]:
        doc_title = source_doc.metadata["title"]
        doc_link = source_doc.metadata["source"]
        source_text += f"• <{doc_link}|{doc_title}>\n"
    return source_text


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
