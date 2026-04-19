import streamlit as st
import google.generativeai as genai

# Получаем ключ из секретов
YOUR_API_KEY = st.secrets["GEMINI_API_KEY"]

# Настраиваем API
genai.configure(api_key=YOUR_API_KEY)
# Создаем инструкцию для Макса (используем тройные кавычки!)
system_prompt = """
Ты — Макс, 16-летний парень из России. 
Ты весёлый и саркастичный. Отвечай всегда на русском языке, коротко и с эмодзи. 
Помогай с уроками как друг, а не как учитель.
"""

# Инициализируем модель (БЕЗ слова "models/")
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction=system_prompt
)

st.title("🤖 Мой ИИ — Макс")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение истории
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле ввода
if prompt := st.chat_input("Напиши Максу..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Прямой вызов генерации
            response = model.generate_content(prompt)
            
            if response.text:
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Макс промолчал... Попробуй еще раз.")
        except Exception as e:
            st.error(f"Ошибка: {e}")
