
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from streamlit_extras.add_vertical_space import add_vertical_space
import time
import base64

def get_download_link(data):
    # Transform data to base64 string
    data_b64 = base64.b64encode(data).decode()

    # Create download link
    href = f'<a href="data:file/txt;base64,{data_b64}" download="chat_history.txt">Download Chat History</a>'

    return href


def get_pdf_text(pdf_docs):
    
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text


def get_text_chunks(text):
    
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=700,
        chunk_overlap=300,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks,progress_bar,time_text):
    batch_size = 90
    delay = 60 
    batches = [text_chunks[i:i + batch_size] for i in range(0, len(text_chunks), batch_size)]
    
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=batches[0], embedding=embeddings)
    for i, batch in enumerate(batches[1:], start=1):  # start from 1 because the first batch is already added
        vectorstore.add_texts(batch)
        
        # Update the progress bar
        progress = (i + 1) / len(batches)
        progress_bar.progress(progress)
        time_text.text(f"Remaining time complete: {len(batches)-i} minute")
        
        time.sleep(delay)
    progress_bar.empty()
    time_text.empty()

    return vectorstore


def get_conversation_chain(vectorstore):
    
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            with st.chat_message("user"):  
                st.write(f" You:**\n {message.content}")
        else:
            with st.chat_message("assistant"):
                st.write(f" Bot:**\n {message.content}")


def main():
    
    load_dotenv()

    st.set_page_config(page_title="Chat with your PDFs", page_icon=":books:")
    st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        
    </style>
""", unsafe_allow_html=True)


    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with your PDF")
    
        

    with st.sidebar:
        st.subheader("📚 My PDFs")
        pdf_docs = st.file_uploader(
            "Upload the document", accept_multiple_files=True, type="pdf")

        if st.button("Process"):
            with st.spinner("Processing..."):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                progress_bar = st.progress(0)
                time_text = st.empty()
                vectorstore = get_vectorstore(text_chunks,progress_bar,time_text)
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)
            st.success("Embedding completed!")

        add_vertical_space(5)
        
    
        
    user_question_placeholder = st.empty()
    user_question = user_question_placeholder.chat_input("Ask a question",key="userPrompt")
    if user_question:
        handle_userinput(user_question)
    if st.button("Download Chat History"):
        st.markdown(get_download_link(st.session_state.chat_history), unsafe_allow_html=True)
        


if __name__ == '__main__':
    main()

