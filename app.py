import streamlit as st
import openai


# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
        ]


# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages
    )

    bot_message = response.choices[0].message
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構。
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"

        if getattr(message, "role", "") == "assistant":  # getattrを使用して安全に属性を取得
            speaker = "🤖"

        if isinstance(message, dict):
            # 辞書であれば、キーを使ってアクセス
            content = message['content']
        else:
            # 辞書でなければ、オブジェクトの属性を使ってアクセス
            content = message.content
        st.write(speaker + ": " + content)
