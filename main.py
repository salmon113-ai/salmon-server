import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages.chat import ChatMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from prompts.prompt_loader import load_prompt
from retriver import create_retriever

load_dotenv()

st.set_page_config(page_title="Salmon Project #1", page_icon="🐟")
st.title("🐟Salmon Project #1")

if not os.path.exists(".cache"):
    os.mkdir(".cache")

if not os.path.exists(".cache/files"):
    os.mkdir(".cache/files")

if not os.path.exists(".cache/embeddings"):
    os.mkdir(".cache/embeddings")


if "messages" not in st.session_state:
    st.session_state["messages"] = []

def print_message():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)
        
def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

@st.cache_resource(show_spinner="업로드한 파일을 처리 중입니다...")
def embed_file(file):
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)

    return create_retriever(file_path)


def format_doc(document_list):
    return "\n\n".join([doc.page_content for doc in document_list])


def create_chain(retriever, prompt):
    # LM studio에서 모델 선택 후 Local server 기동 필요
    llm = ChatOpenAI(model_name="teddylee777/EEVE-Korean-Instruct-10.8B-v1.0-gguf/EEVE-Korean-Instruct-10.8B-v1.0-Q4_0.gguf",
        base_url="http://localhost:1234/v1", api_key="lm-studio")

    return (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )


with st.sidebar:
    # 파일 업로드
    uploaded_file = st.file_uploader("파일 업로드", type=["pdf"])
    clear_btn = st.button("대화내용 초기화", type="primary", use_container_width=True)
    # tab1, tab2 = st.tabs(["prompt", "preset"])
    # prompt = """당신은 친절한 AI 어시스턴트 입니다. 사용자의 질문에 간결하게 답변해 주세요."""
    # user_text_prompt = tab1.text_area("프롬프트", value=prompt)
    # user_text_apply_btn = tab1.button("프롬프트 적용", key="prompt_apply", use_container_width=True)
    # if user_text_apply_btn:
    #     st.warning('작성한 프롬프트가 적용되었습니다.', icon="👍")
    #     prompt_template = user_text_prompt + "\n\n#Question:\n{question}\n\n#Answer:"
    #     prompt = PromptTemplate.from_template(prompt_template)
    #     st.session_state["chain"] = create_chain(, prompt)
    #
    # user_selected_prompt = tab2.selectbox("프리셋 선택", ["summary", "emoji"])
    # user_selected_apply_btn = tab2.button("프롬프트 적용", key="preset_prompt_apply", use_container_width=True)
    # if user_selected_apply_btn:
    #     st.warning(f"{user_selected_prompt} 프롬프트가 적용되었습니다.", icon="👍")
    #     prompt = load_prompt(f"prompts/{user_selected_prompt}.yaml", encoding="utf8")
    #     st.session_state["chain"] = create_chain(None, prompt)

if uploaded_file:
    # 파일 업로드 후 retriever 생성 (작업시간이 오래 걸릴 예정...)
    retriever = embed_file(uploaded_file)
    prompt = load_prompt(f"prompts/rag.yaml", encoding="utf8")
    chain = create_chain(retriever, prompt)
    st.session_state["chain"] = chain

if clear_btn:
    retriever = st.session_state["messages"].clear()

user_input = st.chat_input("궁금한 내용을 물어보세요.")
warning_msg = st.empty()

print_message()

if user_input:
    chain = st.session_state["chain"]

    if chain is not None:
        add_message("user", user_input)
        st.chat_message("user").write(user_input)

        with st.chat_message("assistant"):
            chat_container = st.empty()

            stream_response = st.session_state["chain"].stream(
                user_input
            )

            ai_answer = ""
            for chunk in stream_response:
                ai_answer += chunk
                chat_container.markdown(ai_answer)
            add_message("assistant", ai_answer)

    else:
        # 파일을 업로드 하라는 경고 메시지 출력
        warning_msg.error("파일을 업로드 해주세요.")