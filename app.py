import streamlit as st
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

# --- Page Configuration ---
st.set_page_config(
    page_title="LucidCode 🪄",
    page_icon="🪄",
    layout="wide",
)

# --- Load API Key ---
load_dotenv()

# --- Session State Initialization ---
if 'translation_result' not in st.session_state:
    st.session_state.translation_result = None
if 'explanation_result' not in st.session_state:
    st.session_state.explanation_result = None
if 'original_code' not in st.session_state:
    st.session_state.original_code = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''

# --- Sidebar for API Key Input ---
with st.sidebar:
    st.header("Configuration")
    st.markdown("Enter your Groq API key below to get started. You can get a free key from [GroqCloud](https://console.groq.com/keys).")
    
    user_api_key = st.text_input(
        "Groq API Key:", 
        type="password", 
        placeholder="gsk_...",
        help="Your key is used only for this session and is not stored."
    )
    
    if user_api_key:
        st.session_state.api_key = user_api_key
        st.success("API Key accepted!", icon="✅")

# --- AI Model Initialization ---
llm = None
api_key_to_use = st.session_state.api_key or os.getenv("GROQ_API_KEY")

if api_key_to_use:
    llm = ChatGroq(
        groq_api_key=api_key_to_use,
        temperature=0,
        model_name="llama3-70b-8192"
    )

# --- UI Layout ---
st.markdown("<h1>LucidCode &#x1FA84;</h1>", unsafe_allow_html=True)
st.markdown("Your AI-powered partner for translating, explaining, and improving code.")
st.markdown("---")

# --- Code Translation Section ---
st.header("1. Translate & Explain Your Code")

supported_languages = ["Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "C", "PHP", "R", "SQL", "HTML", "CSS"]

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Source Language", supported_languages)
    source_code = st.text_area("Paste your code here:", height=300, key="source_code_input")

with col2:
    target_lang = st.selectbox("Target Language", supported_languages)
    if st.button("Translate & Explain", type="primary", use_container_width=True):
        if not llm:
            st.warning("Please enter your Groq API Key in the sidebar to begin.")
        elif source_code.strip():
            with st.spinner("The AI is analyzing your code... this may take a moment."):

                # --- SPECIAL HANDLING FOR HTML & CSS ---
                if target_lang in ["HTML", "CSS"]:
                    prompt = f"""
                    You are an expert programmer and code-to-web converter.  
                    The user has given you {source_lang} code, and they want to see it represented as a webpage in {target_lang}.  

                    Your task:
                    - If {target_lang} is **HTML**, generate a webpage that visually represents what the original code does or outputs.  
                    - If {target_lang} is **CSS**, create styles that could represent or enhance the behavior/output of the original code.  
                    - Keep it clean, semantic, and enclosed in a proper markdown code block.  

                    Provide your response in two distinct parts separated by `---EXPLANATION---`.

                    Part 1: The {target_lang} code.  
                    Part 2: A short explanation of how this {target_lang} version represents the original code.  

                    Original Code ({source_lang}):
                    ```
                    {source_code}
                    ```
                    """
                else:
                    prompt = f"""
                    You are an expert programmer and code translator. Your task is to translate a code snippet from {source_lang} to {target_lang} and provide a clear explanation.

                    You must provide your response in two distinct parts separated by a specific delimiter `---EXPLANATION---`.

                    Part 1: The translated code block. The code should be clean, idiomatic for the target language, and enclosed in a markdown code block.  
                    Part 2: A high-level explanation of what the code does. This should be a concise summary, not a line-by-line analysis.

                    Original Code ({source_lang}):
                    ```
                    {source_code}
                    ```

                    Translate this code to {target_lang}.
                    """

                response = llm.invoke(prompt)
                full_response = response.content

                if "---EXPLANATION---" in full_response:
                    parts = full_response.split("---EXPLANATION---", 1)
                    st.session_state.translation_result = parts[0].strip()
                    st.session_state.explanation_result = parts[1].strip()
                else:
                    st.session_state.translation_result = full_response
                    st.session_state.explanation_result = "The AI did not provide a separate explanation."
                
                st.session_state.original_code = source_code
                st.session_state.chat_history = []

    if st.session_state.translation_result:
        # Extract the code from the markdown block for st.code
        code_to_display = st.session_state.translation_result.split('```')[1].split('\n', 1)[1] if '```' in st.session_state.translation_result else st.session_state.translation_result
        st.code(code_to_display, language=target_lang.lower())

# --- Display Explanation ---
if st.session_state.explanation_result:
    st.subheader("Code Explanation")
    st.markdown(st.session_state.explanation_result)
    st.markdown("---")

# --- Conversational Chat Section ---
if st.session_state.translation_result:
    st.header("2. Chat With Your Code")
    
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    if user_question := st.chat_input("Ask a question or ask for suggestions..."):
        st.session_state.chat_history.append(("user", user_question))
        with st.chat_message("user"):
            st.markdown(user_question)
        
        with st.spinner("Thinking..."):
            chat_prompt = f"""
            You are an AI coding assistant. 
            A user will provide a piece of code, translation, or ask follow-up questions. 
            Your role is to answer ANY question related to the given code, its language, or its functionality. 

            You must:
            - Explain what the code does, including syntax, logic, and language-specific details.  
            - Answer questions about how the code works, why it is written that way, and what each part means.  
            - Provide improvements, optimizations, and best practices when relevant.  
            - Help debug errors, explain error messages, and suggest fixes.  
            - Clarify differences between versions of the language or libraries if asked.  
            - Never refuse questions as long as they are about the code, its language, or improvements.  
            - Keep explanations clear, concise, and beginner-friendly, but provide depth if the user asks for advanced details.

            Your goal is to be a reliable, all-in-one coding guide for the user’s provided code and their related questions.

            --- CONTEXT ---
            Original Code ({source_lang}):
            ```
            {st.session_state.original_code}
            ```

            Translated Code ({target_lang}):
            ```
            {st.session_state.translation_result}
            ```

            --- CHAT HISTORY ---
            {st.session_state.chat_history}

            --- USER'S NEW QUESTION ---
            {user_question}
            """
            
            # FIX: use chat_prompt instead of undefined prompt
            ai_response = llm.invoke(chat_prompt).content
            
            st.session_state.chat_history.append(("assistant", ai_response))
            with st.chat_message("assistant"):
                st.markdown(ai_response)
