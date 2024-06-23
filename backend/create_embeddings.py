from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter , CharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.embeddings.ollama import OllamaEmbeddings 
from langchain.vectorstores.chroma import Chroma 
from langchain_community.embeddings.bedrock import BedrockEmbeddings
# from langchain_community.embeddings import Gpt4AllEmbeddings
# from gpt4all import GPT4AllEmbeddings
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain.embeddings import VoyageEmbeddings



def load_document():
    document_loader = PyMuPDFLoader("rulebook.pdf")
    return document_loader.load()

def loadJson():
    loader = JSONLoader(
        file_path = "data.json",
        jq_schema='.laptops',
        text_content=False
    )
    print(type(loader.load()))
    return loader.load()


def split_document(document: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 20,
        chunk_overlap = 10,
        length_function = len , 
        is_separator_regex = False 
    )

    return text_splitter.split_documents(document)



def get_embedding():
    # embeddings = OllamaEmbeddings(model = 'nomic-embed-text')
    embeddings =  GPT4AllEmbeddings(model_name = "all-MiniLM-L6-v2.gguf2.f16.gguf")
    # embeddings = VoyageEmbeddings(model="voyage-01", batch_size=8 , voyage_api_key = "pa-CxiGUeuPQR20R2MxFApTOgz2Qy84RGOzpaSUGQ1jkn4")
    # embeddings = BedrockEmbeddings(credetial_profile_name = "default", region_name = "us-east-1")
    return embeddings 

def chunk_ids(chunks):


    index = 0
    last_page = None
    ids = []
    for chunk in chunks:
        page = chunk.metadata.get("page")
        source = chunk.metadata.get("source")
        if page!= last_page:
            index = 0
            last_page = page
        else:
            index+=1
        new_id = f"{source}:{page}:{index}"
        chunk.metadata['id'] = new_id 
        ids.append(new_id)
    # print(ids)
    return chunks , ids

def chunkIdJson(chunks):
    i = 0 
    ids =[]
    print(chunks)
    for i in chunks:
        print(i)
    


def add_to_chroma(chunks : list[Document]):
    
    db = Chroma(
        persist_directory = "chroma" , embedding_function =  get_embedding()
    )
    print("here")
    # chunk_with_ids, ids = chunk_ids(chunks)
    ids = chunkIdJson(chunks)

    db.add_documents(chunks , ids = [str(x) for x in range(len(chunks))] )
    print("here")
    db.persist()

if __name__ == "__main__":
    rulebook = loadJson()
    # chunks = split_document(rulebook)
    print(rulebook)
    text_splitter = CharacterTextSplitter(
        chunk_size = 30,
        chunk_overlap = 5,
       
    )
    chunks = text_splitter.split_documents(rulebook)
    print(chunks)


    add_to_chroma(chunks)

    print("success")

# print( 'the pdf is', chunks[0])

