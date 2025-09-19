import streamlit as st
import json
import random
import textwrap
import google.generativeai as genai
import os

# Set page config with religious theme
st.set_page_config(
    page_title="Christian Chatbot 🙏",
    page_icon="✝️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for spiritual design
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f9f7f0 0%, #e8f4f8 100%);
        font-family: 'Georgia', serif;
    }
    .header {
        text-align: center;
        color: #2c3e50;
        padding: 2rem 0;
        background: linear-gradient(135deg, #8e9eab 0%, #eef2f3 100%);
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header h1 {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        color: #34495e;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .header h2 {
        font-size: 1.2rem;
        font-weight: normal;
        color: #7f8c8d;
        margin: 0.5rem 0 0 0;
    }
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stChatMessage {
        border-radius: 15px;
        margin: 1rem 0;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stChatMessage.user {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 5px solid #1976d2;
    }
    .stChatMessage.assistant {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        border-left: 5px solid #7b1fa2;
    }
    .stChatInput {
        border-radius: 25px;
    }
    .bible-verse {
        font-style: italic;
        color: #7d3c98;
        background: #f4ecf7;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #8e44ad;
    }
    .prayer {
        color: #27ae60;
        background: #eafaf1;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #2ecc71;
    }
    .footer {
        text-align: center;
        color: #7f8c8d;
        margin-top: 2rem;
        font-size: 0.9rem;
    }
    .name-input {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 2rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# NAME INPUT SECTION
# -----------------------------
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if st.session_state.user_name is None:
    st.markdown("""
    <div class="header">
        <h1>PRAISE THE LORD, DEAR!</h1>
        <h2>MAY THE LORD GUIDE YOU!</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="name-input">
        <h3 style='color: #34495e; margin-bottom: 1.5rem;'>Welcome to God's comforting presence! 💖</h3>
        <p style='color: #7f8c8d;'>Please enter your name so I can personalize our conversation:</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user_name = st.text_input("Your Name:", placeholder="Enter your name here...", label_visibility="collapsed")
        
        if st.button("Submit", use_container_width=True):
            if user_name.strip():
                st.session_state.user_name = user_name.strip()
                st.rerun()
            else:
                st.warning("Please enter your name to continue")

    st.stop()

# -----------------------------
# MAIN CHAT INTERFACE (after name is set)
# -----------------------------
user_name = st.session_state.user_name

# Header with personalized greeting
st.markdown(f"""
<div class="header">
    <h1>PRAISE THE LORD, {user_name.upper()}!</h1>
    <h2>MAY THE LORD GUIDE YOU!</h2>
</div>
""", unsafe_allow_html=True)

# Personalized welcome message
st.markdown(f"""
<div style='text-align: center; color: #34495e; margin: 1rem 0;'>
    <p style='font-size: 1.1rem;'>Welcome, {user_name}! I am here to provide biblical encouragement, prayer support, and spiritual guidance through God's word. 💖</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# 1️⃣ Configure API
# -----------------------------
try:
    # Use Streamlit secrets for API key (for deployment)
    GOOGLE_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    
    if not GOOGLE_API_KEY:
        st.error("Please set GEMINI_API_KEY in Streamlit secrets or environment variables")
        st.stop()
    
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.warning("Google AI configuration skipped - using Bible verses only")
    # Continue without Gemini for fallback functionality

# -----------------------------
# 2️⃣ Load Bible verses JSON
# -----------------------------
@st.cache_data
def load_verses():
    try:
        with open("verses.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("verses.json file not found. Please make sure it's in the same directory.")
        return {}
    except json.JSONDecodeError:
        st.error("Error reading verses.json. Please check the file format.")
        return {}

VERSES = load_verses()

# -----------------------------
# 3️⃣ Function to find matching verse
# -----------------------------
def find_matching_verse(user_input):
    if not VERSES:
        return None
        
    user_input_lower = user_input.lower()
    matching_entries = []

    for category, entries in VERSES.items():
        for entry in entries:
            for kw in entry["keywords"]:
                if kw.lower() in user_input_lower:
                    matching_entries.append(entry)
                    break

    if matching_entries:
        return random.choice(matching_entries)
    else:
        return None

# -----------------------------
# 4️⃣ Format message with user's name
# -----------------------------
def format_message(entry, user_name):
    # Personalize the message with user's name
    personalized_message = entry['message'].replace("[User]", user_name)
    return f"📖 **{entry['text']}** - {entry['ref']}\n\n{personalized_message}"

# -----------------------------
# 5️⃣ Enhanced Chatbot with personalized responses
# -----------------------------
def christian_chatbot(user_input, user_name):
    # First try to find matching Bible verse
    entry = find_matching_verse(user_input)
    
    if entry:
        return format_message(entry, user_name)
    else:
        # Fallback to Gemini AI for more general responses
        try:
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"""As a Christian chatbot, provide a brief, comforting, and biblically-based response to {user_name} who said: {user_input}
            Address them by name ({user_name}) and keep it under 3 sentences. Focus on encouragement, faith, and God's love."""
            
            response = model.generate_content(prompt)
            return f"💖 {response.text}"
            
        except Exception:
            # Final fallback if Gemini also fails
            fallback_responses = [
                f"🙏 {user_name}, I'm here to pray with you and encourage you. Could you tell me more about how you're feeling?",
                f"💖 {user_name}, God loves you deeply. Would you like to share what's on your heart?",
                f"✝️ {user_name}, remember that Jesus is always with you. How can I pray for you today?",
                f"📖 {user_name}, sometimes we just need to be still and know that He is God. What's troubling you?"
            ]
            return random.choice(fallback_responses)

# -----------------------------
# 6️⃣ Streamlit Chat Interface
# -----------------------------

# Initialize chat history with personalized welcome
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Peace be with you, {user_name}! 🙏 How can I encourage you today?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input(f"Share your thoughts, {user_name}..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.spinner("Thinking of encouragement..."):
        response = christian_chatbot(prompt, user_name)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Sidebar with user info and controls
with st.sidebar:
    st.header(f"Welcome, {user_name}! ✝️")
    st.markdown(f"""
    **Chatbot Features for you:**
    - 📖 Personalized Bible verses
    - 🙏 Prayer support for {user_name}
    - 💖 Spiritual guidance
    - ✝️ Faith-based comfort
    
    *"The LORD bless you and keep you, {user_name}" - Numbers 6:24*
    """)
    
    # Clear chat button
    if st.button("🔄 Start New Conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": f"Peace be with you, {user_name}! 🙏 How can I encourage you today?"}
        ]
        st.rerun()
    
    # Change name button
    if st.button("✏️ Change Name"):
        st.session_state.user_name = None
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <p>May God's peace be with you always. ✝️💖</p>
</div>
""", unsafe_allow_html=True)