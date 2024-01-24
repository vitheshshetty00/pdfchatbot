# PDF Chatbot

Welcome to PDF Chatbot, an interactive chat application that allows you to engage in conversations with your PDF documents. This application leverages Streamlit as the web framework and integrates seamlessly with various libraries for PDF processing, text splitting, embeddings, and conversational retrieval.

## Installation

#### Clone the Repository:

```bash
git clone https://github.com/vitheshshetty00/pdfchatbot.git
```
#### Install dependencies using pip:
   
   ```bash  
   pip install -r requirements.txt
   ```
#### Set Up Environment Variables:
- Create a .env file in the project's root directory.
- Add the necessary environment variables following the structure in .env.example.
## Usage
To use this chatbot, you need to have python installed on your system and then follow these steps
1. Run the main application file from the terminal or command prompt:
   ```bash
   streamlit run main.py
   ```
2. Upload a PDF file using the file uploader widget.
3. Wait for the PDF to be processed.
4. Once the PDF is processed, you can start interacting with the chatbot.
5. You can also download the processed PDF by clicking on the download button.
## Features
- `Dynamic Handling of PDF Sizes`: PDF Chatbot efficiently processes PDFs of any size, adapting to the content length.
- `Responsive UI`: Streamlit provides a user-friendly interface, making it easy to navigate and interact with the application.
- `Conversational Retrieval`: Engage in natural language conversations with the chatbot, utilizing embeddings for meaningful response

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

**Enjoy chatting with your PDFs using PDF Chatbot!**