import streamlit as st
import requests

# 🌟 Page Config
st.set_page_config(page_title="Fahath Bike AI", page_icon="🏍️", layout="centered")

# 💎 Custom CSS for Glassmorphism & WhatsApp UI
st.markdown("""
<style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d3436 100%);
    }
    
    /* Welcome Header */
    .welcome-text {
        text-align: center;
        color: #00d2ff;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        text-shadow: 2px 2px 10px rgba(0, 210, 255, 0.3);
        margin-bottom: 20px;
    }

    /* Glass Chat Container */
    .chat-bubble {
        padding: 15px;
        border-radius: 20px;
        margin-bottom: 15px;
        max-width: 80%;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .user-msg {
        background: rgba(0, 210, 255, 0.2);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 2px;
    }

    .ai-msg {
        background: rgba(255, 255, 255, 0.1);
        color: #f1f1f1;
        margin-right: auto;
        border-bottom-left-radius: 2px;
    }

    /* 🌊 Water/Glassy Button Effect */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 10px 25px;
        border-radius: 50px;
        backdrop-filter: blur(15px);
        transition: all 0.5s ease;
        position: relative;
        overflow: hidden;
        width: 100%;
    }

    div.stButton > button:hover {
        background: rgba(0, 210, 255, 0.4);
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.6);
        color: white;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# 🏁 Welcome Message
st.markdown('<h1 class="welcome-text">Welcome to Fahath Bike Recommendation</h1>', unsafe_allow_html=True)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages (WhatsApp Style)
for message in st.session_state.messages:
    role_class = "user-msg" if message["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="chat-bubble {role_class}">{message["content"]}</div>', unsafe_allow_html=True)

# User Input Section
user_input = st.text_input("Namma Expert kitta kelunga...", key="user_query", placeholder="Example: 2 lakh budget-la stylish bike?")

if st.button("Get Recommendation 🏍️"):
    if user_input:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 🔗 Flowise Connection (REPLACE WITH YOUR RENDER URL)
        API_URL = "https://fahath-bike-recommendation-ai.onrender.com/api/v1/prediction/YOUR_CHATFLOW_ID"
        
        with st.spinner("Expert processing..."):
            try:
                response = requests.post(API_URL, json={"question": user_input})
                if response.status_code == 200:
                    answer = response.json().get("text", "Error: No response from AI")
                    # Clean the AI output (Single line format as requested)
                    clean_answer = answer.replace("\n", " ").strip()
                    st.session_state.messages.append({"role": "assistant", "content": clean_answer})
                    st.rerun()
                else:
                    st.error("Backend Error! Flowise URL check pannunga.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Type pannunga nanba!")
      
