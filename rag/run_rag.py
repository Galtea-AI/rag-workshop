from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import os
from argparse import ArgumentParser
from dotenv import load_dotenv
load_dotenv()
# Load environment variables from .env file

CHROMA_PATH = "chroma"

with open("rag/prompt_template.txt", "r") as file:
    PROMPT_TEMPLATE = file.read()

def query_rag(query_text, threshold=0.2):
    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < threshold:
        return f"Le pido disculpas, pero no dispongo de información sobre ese asunto."

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    print(f"Context: {context_text}")
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    #print(prompt)

    model = ChatOpenAI()
    response_text = model.predict(prompt)

    return response_text

if __name__ == "__main__":
    parser = ArgumentParser(description="Run RAG")
    parser.add_argument("--query", type=str, help="Query to ask the RAG system")
    parser.add_argument("--threshold", type=float, default=0.2, help="Threshold for similarity search")
    args = parser.parse_args()
    if not args.query:
        raise ValueError("Please provide a query using --query argument")

    response_text = query_rag(args.query, args.threshold)
    print("Response: ", response_text)