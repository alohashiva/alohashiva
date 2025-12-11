import streamlit as st
import google.generativeai as genai

# Cấu hình trang
st.set_page_config(page_title="Trợ lý Đội Nhóm", page_icon="🤖")
st.title("🤖 Chatbot Hỗ Trợ Đội Nhóm")

# 1. Kết nối an toàn với API Key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Chưa nhập API Key! Hãy vào Settings -> Secrets để nhập.")
    st.stop()

# 2. Cấu hình "Bộ não" AI
model = genai.GenerativeModel(
    model_name="gemini-pro", # Bản nhanh và miễn phí
    system_instruction="Bạn là trợ lý ảo hữu ích cho công ty. Trả lời ngắn gọn, chuyên nghiệp."
)

# 3. Lưu lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Hiển thị chat cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Xử lý khi nhập câu hỏi
if prompt := st.chat_input("Nhập câu hỏi..."):
    # Hiện câu hỏi người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI trả lời
    try:
        response = model.generate_content(prompt)
        reply = response.text
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"Lỗi: {e}")
