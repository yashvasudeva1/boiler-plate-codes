import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import config

load_dotenv()

st.set_page_config(page_title="RAG Boilerplate", page_icon="📚")
st.title("📚 RAG Boilerplate")

with st.sidebar:
    st.header("Settings")
    openai_api_key = st.text_input(
        "OpenAI API Key", 
        type="password", 
        value=os.getenv("OPENAI_API_KEY", "")
    )
    
    top_k = st.slider("TOP_K", min_value=1, max_value=10, value=config.TOP_K)
    chunk_size = st.slider("CHUNK_SIZE", min_value=200, max_value=2000, value=config.CHUNK_SIZE)
    
    if st.button("Clear & Re-upload"):
        if "vectorstore" in st.session_state:
            del st.session_state.vectorstore
        if "messages" in st.session_state:
            del st.session_state.messages
        st.rerun()
        
    st.info("Upload a document to get started.")

def process_file(uploaded_file, chunk_size):
    """Save uploaded file temporarily, load it based on extension, and split it into chunks."""
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_path = temp_file.name

    if ext == '.pdf':
        loader = PyPDFLoader(temp_path)
    elif ext == '.txt':
        loader = TextLoader(temp_path)
    elif ext == '.docx':
        loader = Docx2txtLoader(temp_path)
    elif ext == '.csv':
        loader = CSVLoader(temp_path)
    else:
        os.remove(temp_path)
        raise ValueError(f"Unsupported file format: {ext}")

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    splits = text_splitter.split_documents(docs)
    
    os.remove(temp_path)
    return splits

if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
    
    uploaded_file = st.file_uploader("Upload a Document", type=["pdf", "txt", "docx", "csv"])
    
    if uploaded_file and "vectorstore" not in st.session_state:
        with st.spinner("Processing document and creating Vector Store..."):
            splits = process_file(uploaded_file, chunk_size)
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(splits, embeddings)
            st.session_state.vectorstore = vectorstore
            st.success("Document processed and vector store created!")

    if "vectorstore" in st.session_state:
        retriever = st.session_state.vectorstore.as_retriever(
            search_kwargs={"k": top_k}
        )
        
        llm = ChatOpenAI(
            model=config.LLM_MODEL, 
            temperature=config.LLM_TEMPERATURE
        )
        
        prompt = ChatPromptTemplate.from_template("""
        Answer the question based only on the following context:
        {context}
        
        Question: {question}
        
        Answer:
        """)
        
        def format_docs(docs):
            """Format document objects into text strings."""
            return "\n\n".join(doc.page_content for doc in docs)
            
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        st.divider()
        st.subheader("Chat")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        if question := st.chat_input("Ask a question about your document"):
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)
                
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = rag_chain.invoke(question)
                st.markdown(response)
                
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.warning("Please enter your OpenAI API key in the sidebar.")
