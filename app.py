import streamlit as st
import google.generativeai as genai

# 1. Ключ из секретов
YOUR_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=YOUR_API_KEY)

# 2. Настройка Макса
system_prompt = """
Ты — Макс, 16-летний парень из России. 
Ты весёлый и саркастичный. Отвечай всегда на русском языке, коротко и с эмодзи. 
Помогай с уроками как друг.
"""

# 3. Создание модели (используем только проверенные аргументы)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)

st.title("🤖 Мой ИИ — Макс")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Показываем старые сообщения
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Поле ввода
if prompt := st.chat_input("Напиши Максу..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ЧИСТЫЙ ВЫЗОВ БЕЗ ЛИШНИХ ПАРАМЕТРОВ
            response = model.generate_content(prompt)
            
            if response.text:
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Макс молчит. Попробуй обновить страницу.")
        except Exception as e:
            st.error(f"Ошибка: {e}")
