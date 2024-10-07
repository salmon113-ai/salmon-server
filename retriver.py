from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_retriever(file_path):
    # 단계 1: 문서 로드(Load Documents)
    loader = PDFPlumberLoader(file_path)
    docs = loader.load()

    # 단계 2: 문서 분할(Split Documents)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    split_documents = text_splitter.split_documents(docs)

    # 단계 3: 임베딩(Embedding) 생성
    embeddings = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-large-instruct",
        model_kwargs={"device": "cuda"},  # cuda, cpu
        encode_kwargs={"normalize_embeddings": True},
    )

    # 단계 4: DB 생성(Create DB) 및 저장
    vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)

    # 단계 5: 검색기(Retriever) 생성
    retriever = vectorstore.as_retriever()
    return retriever