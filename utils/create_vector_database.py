from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from argparse import ArgumentParser
import openai
from dotenv import load_dotenv
import os
import shutil

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()
#---- Set OpenAI API key 
# Change environment variable name from "OPENAI_API_KEY" to the name given in 
# your .env file.
openai.api_key = os.environ['OPENAI_API_KEY']

CHROMA_PATH = "chroma"
DATA_PATH = "docs"

def generate_data_store(chunk_size=1024, chunk_overlap=256):
    documents = load_documents()
    chunks = split_text(documents, chunk_size, chunk_overlap)
    save_to_chroma(chunks)

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()
    return documents

def split_text(documents: list[Document], chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    #document = chunks[10]
    #print(document.page_content)
    #print(document.metadata)

    return chunks

def clear_chroma_directory(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    clear_chroma_directory(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    parser = ArgumentParser(description="Create vector database")
    parser.add_argument(
        "--chunk_size",
        type=int,
        default=1024,
        help="Chunk size for splitting documents",
    )
    parser.add_argument(
        "--chunk_overlap",
        type=int,
        default=256,
        help="Chunk overlap for splitting documents",
    )
    args = parser.parse_args()
    if not os.path.exists(DATA_PATH):
        raise ValueError(f"Data path {DATA_PATH} does not exist. Please create it and add text files.")
    if not os.listdir(DATA_PATH):
        raise ValueError(f"Data path {DATA_PATH} is empty. Please add text files.")
    if not os.path.exists(CHROMA_PATH):
        os.makedirs(CHROMA_PATH, exist_ok=True)
    
    if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
        print(f"Warning: {CHROMA_PATH} already exists and is not empty. It will be cleared.")
        clear_chroma_directory(CHROMA_PATH)
        # shutil.rmtree(CHROMA_PATH)    
        os.makedirs(CHROMA_PATH, exist_ok=True)

    # Generate the vector database.
    generate_data_store(args.chunk_size, args.chunk_overlap)
    print(f"Vector database created at {CHROMA_PATH} with chunk size {args.chunk_size} and chunk overlap {args.chunk_overlap}.")
