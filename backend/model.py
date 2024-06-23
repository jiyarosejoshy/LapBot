from langchain_community.llms.ollama import Ollama 
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate 
from create_embeddings import get_embedding

PROMPT_TEMPLATE = """
Answer the quesiton based on the following context : {context}
-------
Answer the question based on the above context: {question}
"""


def query(query_text):
    # query_text = input(">>")

    db = Chroma(persist_directory="chroma", embedding_function=get_embedding())
    results = db.similarity_search_with_score(query_text, k=5)

    print("passing template")

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt = prompt_template.format(context=context_text, question=query_text)

    print(prompt)
    model = Ollama(model='mistral')
    response_text = model(prompt)
    print("reacher here")
    print(response_text)

    return response_text

if __name__ == "__main__":
    while True:
        query_input = input(">>")
        response = query(query_input)
        print(response)
