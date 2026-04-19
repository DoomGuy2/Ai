import streamlit as st
import google.generativeai as genai

# Подключаем ключ
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🤖 Макс: Тест связи")

# Упрощаем модель до предела
model = genai.GenerativeModel('gemini-1.5-flash')

if prompt := st.chat_input("Напиши привет"):
    st.chat_message("user").markdown(prompt)
    
    try:
        # Самый базовый вызов
        response = model.generate_content(prompt)
        st.chat_message("assistant").markdown(response.text)
    except Exception as e:
        st.error(f"Ошибка: {e}")
