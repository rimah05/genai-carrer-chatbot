# 🎯 GenAI Chatbot for Personalized Career Advice
# Author: Rima Hazra
# Goal: Use OpenAI/Gemini LLM to suggest personalized career paths, skills, and resources

import streamlit as st
import os

# Attempt to import openai; if not installed, show user-friendly error
try:
    import openai
except ModuleNotFoundError:
    st.error("The 'openai' module is not installed. Please ensure 'openai' is listed in your requirements.txt file.")
    st.stop()

# ---- CONFIGURATION ----
if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
elif "OPENAI_API_KEY" in os.environ:
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
else:
    st.error("OpenAI API key not found. Please set it in Streamlit secrets or environment variables.")
    st.stop()

# ---- UI: Streamlit Layout ----
st.set_page_config(page_title="GenAI Career Advisor", layout="centered")
st.title("🔮 AI Career Advisor")
st.markdown("_Get career guidance powered by GenAI!_")

# ---- USER INPUT ----
user_input = st.text_area("✍️ Describe your background, interests, and goals:")

# ---- PROMPT TEMPLATE ----
def build_prompt(user_text):
    return f"""
You are a career recommendation assistant.
Based on the user's background and interests, suggest:
1. 2-3 suitable career paths
2. In-demand tools/technologies for each
3. Top online resources or courses to start
4. Final tips or motivational line

User Profile:
{user_text}

Respond clearly with bullet points.
"""

# ---- GENERATE RESPONSE ----
if st.button("🎯 Get Recommendations") and user_input.strip():
    with st.spinner("Thinking..."):
        try:
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful career guide."},
                    {"role": "user", "content": build_prompt(user_input)}
                ],
                temperature=0.7,
                max_tokens=500
            )
            reply = chat_completion.choices[0].message.content
            st.success("Here’s your personalized advice:")
            st.markdown(reply)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---- FOOTER ----
st.markdown("---")
st.markdown("Created by Rima Hazra | Powered by OpenAI")
