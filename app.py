import streamlit as st
import google.generativeai as genai

# Подключаем ключ из Secrets
YOUR_API_KEY = st.secrets["GEMINI_API_KEY"]

# Настраиваем API (принудительно через стабильный метод)
genai.configure(api_key=YOUR_API_KEY)
system_prompt = """
Ты — Макс, 16-летний парень из России. 
Ты весёлый и саркастичный. Отвечай коротко и с эмодзи. 
Отвечай всегда на русском языке. 
Помогай с уроками по математике, информатике и английскому, но не как учитель, а как друг.
"""

# ВАЖНО: пробуем создать модель БЕЗ префикса models/
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)

st.title("🤖 Мой ИИ — Тест")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Напиши Максу..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Используем упрощенный вызов
            response = model.generate_content(prompt)
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Ошибка: {e}")
