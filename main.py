import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

st.title("🐟Salmon Project #1")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

def print_message():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)
        
def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

def create_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 친절한 AI 어시스턴트입니다. 질문에 짧게 답변하세요."),
        ("user", "#Question:\n{question}")
    ])
    # LM studio에서 모델 선택 후 Local server 기동 필요
    llm = ChatOpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    output_parser = StrOutputParser()
    
    chain = prompt | llm | output_parser
    return chain
    
    
user_input = st.chat_input("궁금한 내용을 물어보세요.")

print_message()

if user_input:
    st.chat_message("user").write(user_input)
    
    chain = create_chain()
    ai_answer = chain.invoke({"question": user_input})
    st.chat_message("assistant").write(ai_answer)
    
    add_message("user", user_input)
    add_message("assistant", user_input)
    
