from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

CUSTOM_PROMPT_TEMPLATE = """
You are an expert on Salesforce CME, whose job is to answer questions to help resolve customer issues. 
Use the following pieces of context to answer the question at the end. Add as much information as available, and try to provide a step-wise troubleshooting plan.
If the information is insufficient, ask questions that can help return useful steps. Try to stay relevant to the page title. Do not assume, ask for clarity.
Try to mention related past investigations along with any diagnostic tool that can be helpful.
Reply in points, not more than 7.
If you don't know the answer, say that you don't know, don't try to make up an answer.
 

{context}

Question: {question}
Helpful Answer:"""
DATABASE_FOLDER = 'embedding_db';


class ChatClient: 
    def __init__(self) -> None:
        CUSTOMPROMPT = PromptTemplate(
            template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context", "question"]
        )
        retriever = self.__get_retriever_from_db()
        memory = ConversationBufferMemory(memory_key="chat_history", input_key='question', output_key='answer', return_messages=True)
        self.__qa_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(temperature=0.0,  
                        model_name='gpt-3.5-turbo'), 
            retriever=retriever,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": CUSTOMPROMPT},
            memory=memory
            )

    def chat(self, query):
        return self.__qa_chain({"question": query})
    
    def __get_retriever_from_db(self):
        vectordb = Chroma(persist_directory=DATABASE_FOLDER, 
                    embedding_function=OpenAIEmbeddings())
        return vectordb.as_retriever(search_kwargs={"k":4})
