import streamlit as st
from modules.rag_pipeline import load_vectorstore, retrieve_context, create_vectorstore_from_file
from modules.classifier import classify_query
from modules.response_router import generate_response
from modules.memory import get_chat_history
import os
import shutil

st.set_page_config(page_title="Smart Support Copilot using RAG and Dynamic Query Routing")

st.title("📱 Smart Support Copilot using RAG and Dynamic Query Routing")

# -----------------------------
# SESSION STATE
# -----------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

# Load vector DB
vectorstore = load_vectorstore()
# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("⚙️ Controls")
st.sidebar.info("Supported formats: PDF, TXT")
uploaded_file = st.sidebar.file_uploader(
    "Upload Manual / FAQ",
    type=["txt", "pdf"]
)
# -----------------------------
# PROCESS NEW FILE
# -----------------------------

if uploaded_file is not None:

    # Avoid rebuilding repeatedly
    if uploaded_file.name != st.session_state.uploaded_file_name:

        # Save uploaded file
        os.makedirs("data", exist_ok=True)

        file_path = os.path.join(
            "data",
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        try:
            # Create vectorstore
            create_vectorstore_from_file(file_path)
            st.sidebar.success("File processed successfully!")
        except Exception as e:
            st.sidebar.error(str(e))         

        # Store filename
        st.session_state.uploaded_file_name = uploaded_file.name

        # Reset chat when new file uploaded
        st.session_state.chat_history = []

        st.sidebar.success(
            f"Uploaded: {uploaded_file.name}"
        )
# -----------------------------
# CLEAR CHAT BUTTON
# -----------------------------

if st.sidebar.button("🧹 Clear Chat"):

    st.session_state.chat_history = []

    st.sidebar.success("Chat history cleared!")        
# -----------------------------
# REMOVE FILE BUTTON
# -----------------------------

if st.sidebar.button("❌ Remove Uploaded File"):

    # Remove uploaded files
    if os.path.exists("data"):

        shutil.rmtree("data")

    # Remove vectorstore
    if os.path.exists("vectorstore/faiss_index"):

        shutil.rmtree("vectorstore/faiss_index")

    # Recreate empty data folder
    os.makedirs("data", exist_ok=True)

    # Reset session
    st.session_state.chat_history = []
    st.session_state.uploaded_file_name = None

    st.sidebar.success("Uploaded file removed!")
    
# User input
user_query = st.chat_input("Ask your question...")

if user_query:
    if vectorstore is None:
        st.warning("⚠️ No knowledge base found. Please upload a valid PDF or TXT file first.")
        st.sidebar.error("❌ No knowledge base loaded")
    else:
        st.sidebar.success("✅ Knowledge base ready")
    
        # Classification
        query_type = classify_query(user_query)
        # Save user message
        st.session_state.chat_history.append(
            {"role": "user", "content": user_query, "query_type": query_type}
        )        
        # Retrieve docs
        retrieved_docs = retrieve_context(vectorstore, user_query)
    
        # Generate response
        response = generate_response(
            query=user_query,
            query_type=query_type,
            docs=retrieved_docs,
            chat_history=st.session_state.chat_history
        )
    
        # Save assistant response
        st.session_state.chat_history.append(
            {"role": "assistant", "content": response}
        )

# Display history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Show query classification
        if msg["role"] == "user" and "query_type" in msg:

            st.caption(
                f"🧠 Query Type: {msg['query_type'].upper()}"
            )