import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

load_dotenv()

class DocumentProcessor:
    def __init__(self):
        # Using OpenAI embedding models for strong Arabic language support
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Smart text splitting: Arabic punctuation is used as separators
        # to avoid breaking semantic meaning
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", "؟", "!", "،", " ", ""]
        )

    def load_and_split(self, file_path):
        ext = os.path.splitext(file_path)[-1].lower()
        
        if ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif ext in ['.doc', '.docx']:
            loader = Docx2txtLoader(file_path)
        elif ext == '.txt':
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        
        return chunks
