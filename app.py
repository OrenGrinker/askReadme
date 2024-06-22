import streamlit as st
from utils import fetch_readme_content, analyze_readme_content
from config import CSS

# Apply custom CSS
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
# Streamlit app
st.title("GitHub README Analyzer")
st.write("Enter a GitHub project link to analyze its README file content.")

# Sidebar for API key input and other settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("API Key", type="password")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 100, 2000, 1000)

# Input field for GitHub project link
github_link = st.text_input("GitHub Project Link", "https://github.com/username/repo-name")

chat_history = st.session_state.get('chat_history', [])
first_analysis_done = st.session_state.get('first_analysis_done', False)

if st.button("Analyze README"):
    readme_content = fetch_readme_content(github_link)
    if readme_content:
        st.write("### README Content:")
        st.code(readme_content, language="markdown")

        with st.spinner("Analyzing README..."):
            analysis_result = analyze_readme_content(readme_content, api_key, temperature, max_tokens, chat_history)
            if isinstance(analysis_result, list) and hasattr(analysis_result[0], 'text'):
                analysis_result = analysis_result[0].text  # Extract text from the TextBlock
            formatted_result = analysis_result.replace("\n", "<br>").replace("###", "<h3>").replace("##",
                                                                                                    "<h2>").replace("#",
                                                                                                                    "<h1>")
            st.markdown(
                "<div style='padding:10px;border:1px solid #ddd;border-radius:5px;background-color:#f9f9f9;'>"
                f"{formatted_result}"
                "</div>",
                unsafe_allow_html=True
            )
            chat_history.append({"role": "assistant", "content": [{"type": "text", "text": analysis_result}]})
            st.session_state.chat_history = chat_history
            st.session_state.first_analysis_done = True
            st.session_state.readme_content = readme_content

if st.session_state.get('first_analysis_done', False):
    st.write("### Continue the Conversation")
    user_input = st.text_input("Your message")

    if st.button("Send"):
        if user_input:
            chat_history.append({"role": "user", "content": [{"type": "text", "text": user_input}]})
            st.session_state.chat_history = chat_history
            readme_content = st.session_state.get('readme_content', "")
            with st.spinner("Generating response..."):
                response = analyze_readme_content(readme_content, api_key, temperature, max_tokens, chat_history)
                if isinstance(response, list) and hasattr(response[0], 'text'):
                    response_text = response[0].text  # Extract text from the TextBlock
                else:
                    response_text = response
                formatted_response = response_text.replace("\n", "<br>").replace("###", "<h3>").replace("##",
                                                                                                        "<h2>").replace(
                    "#", "<h1>")
                st.markdown(
                    "<div style='padding:10px;border:1px solid #ddd;border-radius:5px;background-color:#f9f9f9;'>"
                    f"{formatted_response}"
                    "</div>",
                    unsafe_allow_html=True
                )
                chat_history.append({"role": "assistant", "content": [{"type": "text", "text": response_text}]})
                st.session_state.chat_history = chat_history

# Display chat history
if chat_history:
    st.write("### Chat History")
    for chat in chat_history:
        if chat['role'] == 'user':
            st.write(f"**You:** {chat['content'][0]['text']}")
        else:
            st.write(f"**Assistant:** {chat['content'][0]['text']}")