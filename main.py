import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from prompts.prompt_loader import load_prompt

st.title("🐟Salmon Project #1")
        
if "messages" not in st.session_state:
    st.session_state["messages"] = []

def print_message():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)
        
def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

def create_chain(prompt):
    # LM studio에서 모델 선택 후 Local server 기동 필요
    llm = ChatOpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    output_parser = StrOutputParser()
    
    return prompt | llm | output_parser
    
with st.sidebar:
    tab1, tab2 = st.tabs(["프롬프트", "프리셋"])
    prompt = """당신은 친절한 AI 어시스턴트 입니다. 사용자의 질문에 간결하게 답변해 주세요."""
    user_text_prompt = tab1.text_area("프롬프트", value=prompt)
    user_text_apply_btn = tab1.button("프롬프트 적용", key="prompt_apply")
    if user_text_apply_btn:
        tab1.markdown(f"✅ 작성한 프롬프트가 적용되었습니다")
        prompt_template = user_text_prompt + "\n\n#Question:\n{question}\n\n#Answer:"
        prompt = PromptTemplate.from_template(prompt_template)
        st.session_state["chain"] = create_chain(prompt)

    user_selected_prompt = tab2.selectbox("프리셋 선택", ["summary", "emoji"])
    user_selected_apply_btn = tab2.button("프롬프트 적용", key="preset_prompt_apply")
    if user_selected_apply_btn:
        tab2.markdown(f"✅ 프리셋 프롬프트가 적용되었습니다")
        prompt = load_prompt(f"prompts/{user_selected_prompt}.yaml", encoding="utf8")
        st.session_state["chain"] = create_chain(prompt)

    clear_btn = st.button("대화내용 초기화", type="primary", use_container_width=True)

if clear_btn:
    retriever = st.session_state["messages"].clear()

user_input = st.chat_input("궁금한 내용을 물어보세요.")

print_message()

if "chain" not in st.session_state:
    prompt = load_prompt(f"prompts/general.yaml", encoding="utf8")
    st.session_state["chain"] = create_chain(prompt)

if user_input:
    add_message("user", user_input)
    st.chat_message("user").write(user_input)

    with st.chat_message("assistant"):
        chat_container = st.empty()

        stream_response = st.session_state["chain"].stream(
            {"question": user_input}
        )

        ai_answer = ""
        for chunk in stream_response:
            ai_answer += chunk
            chat_container.markdown(ai_answer)
        add_message("assistant", ai_answer)
