from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.documents import Document
from pypdf.errors import PdfStreamError
import fitz 
from dotenv import load_dotenv
import os

load_dotenv()

VECTOR_PATH = "vectorstore/faiss_index"


def get_embeddings():

    return AzureOpenAIEmbeddings(
        azure_deployment=os.getenv(
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
        ),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )
def load_document(file_path):
    try:
        # ---------------- PDF ----------------
        if file_path.lower().endswith(".pdf"):
            doc = fitz.open(file_path)
            documents = []
            for page_num, page in enumerate(doc):
                page_text = page.get_text()
                if page_text.strip():
                    documents.append(
                        Document(
                            page_content=page_text,
                            metadata={
                                "source": file_path,
                                "page": page_num + 1
                            }
                        )
                    )
            return documents
        # ---------------- TXT ----------------
        else:
            loader = TextLoader(file_path, encoding="utf-8")
            return loader.load()
    except Exception as e:
        raise ValueError(f"❌ Failed to load file: {str(e)}")      
        
def create_vectorstore_from_file(file_path):

    documents = load_document(file_path)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    docs = splitter.split_documents(documents)

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(
        docs,
        embeddings
    )

    # Create folder if not exists
    os.makedirs("vectorstore", exist_ok=True)

    # Save FAISS index
    vectorstore.save_local(VECTOR_PATH)

    return vectorstore
def load_vectorstore():

    embeddings = get_embeddings()
    try:
        # If vectorstore does not exists return None
        if not os.path.exists(VECTOR_PATH):
            return None
        # Else load vectorstrore    
        return FAISS.load_local(
            VECTOR_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    except Exception as e:
        print(f"Vectorstore load failed: {e}")
        return None

    # No vectorstore exists
    return None


def retrieve_context(vectorstore, query):
    if vectorstore is None:
        return ""
    docs = vectorstore.similarity_search(query, k=3)
    return "\n\n".join([doc.page_content for doc in docs])