import streamlit as st
import google.generativeai as genai

# ================== НАСТРОЙКИ ТВОЕГО ИИ ==================
# Теперь ключ берется из секретов Streamlit Cloud для безопасности
YOUR_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=YOUR_API_KEY)

# Здесь ты можешь менять характер, просто редактируя текст ниже
system_prompt = """
Ты — Макс, 16-летний парень из России. 
Ты весёлый, саркастичный, любишь игры (особенно CS2 и Roblox), мемы.
Отвечай всегда на русском языке, коротко и по делу, с эмодзи и шутками.
Помогай с уроками по математике, информатике и английскому, но не как учитель, а как друг.
Если я грущу — подбодри.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)

# ================== ИНТЕРФЕЙС ==================
st.title("🤖 Мой ИИ — Тест")
st.caption("Это полностью мой собственный бот")

# Память разговора
if "messages" not in st.session_state:
    st.session_state.messages = []

# Показываем всю историю
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле ввода
if prompt := st.chat_input("Напиши что-нибудь..."):
    # Добавляем сообщение пользователя
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Получаем ответ от Gemini
    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            # Отправляем всю историю чата, чтобы бот всё помнил
            response = model.generate_content(prompt)
            answer = response.text
            st.markdown(answer)
    
    # Сохраняем ответ в память
    st.session_state.messages.append({"role": "assistant", "content": answer})
