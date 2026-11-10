
import time
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from app.core.config import get_settings

settings = get_settings()

_embeddings = None
_vectorstore = None

# Incase we want to run different kinds of embedding models..
# It is solely for the future so we don't have to code manually again (Thinking ahead)
EMBEDDING_DIMENSIONS = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
    "text-embedding-ada-002": 1536,
    "all-minilm-16-v2": 384
}


# Easy Python Function to take model name and return dimension
def get_embedding_dimension(model_name: str | None = None) -> int:

    name = (model_name or settings.embedding_model or "").strip()

    if not name:
        raise RuntimeError("Embedding model is not configured.")

    normalized = name.lower()

    if normalized in EMBEDDING_DIMENSIONS:
        return EMBEDDING_DIMENSIONS[normalized]  # attribute for the key "normalized"

    if "text-embedding-3-small" in normalized:
        return 1536

    if "text-embedding-3-large" in normalized:
        return 3072

    if "text-embedding-ada-002" in normalized:
        return 1536

    if "all-minilm" in normalized:
        return 384

    raise ValueError(
        f"Unsupported embedding model '{model_name or settings.embedding_model}' for Pinecone."
        " Add the matching dimension to EMBEDDING_DIMENSIONS."
    )


# Initialize and cache the embedding model
def get_embeddings():

    global _embeddings

    if _embeddings is None:  # FIXED: Use 'is None', not 'in None'

        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing")

        _embeddings = OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.openai_api_key
        )

    return _embeddings


def ensure_index():

    if not settings.pinecone_api_key:
        raise RuntimeError("PINECONE_API_KEY is missing.")

    desired_dimension = get_embedding_dimension()

    pc = Pinecone(api_key=settings.pinecone_api_key)

    names = [x["name"] for x in pc.list_indexes()]

    if settings.pinecone_index_name in names:

        index_info = pc.describe_index(settings.pinecone_index_name)

        current_dimension = getattr(index_info, "dimension", None)

        if current_dimension is None and isinstance(index_info, dict):
            current_dimension = index_info.get("dimension")

        if current_dimension is not None and current_dimension != desired_dimension:

            print(
                f"Dimension mismatch: Existing = {current_dimension}, "
                f"Required = {desired_dimension}"
            )

            # WARNING: Deleting an index permanently removes its stored vectors.
            pc.delete_index(name=settings.pinecone_index_name)

            while settings.pinecone_index_name in [
                x["name"] for x in pc.list_indexes()
            ]:
                time.sleep(1)

    if settings.pinecone_index_name not in [
        x["name"] for x in pc.list_indexes()
    ]:

        pc.create_index(
            name=settings.pinecone_index_name,
            dimension=desired_dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

        while not pc.describe_index(
            settings.pinecone_index_name
        ).status["ready"]:
            time.sleep(1)

    return pc.Index(settings.pinecone_index_name)


# Store all the vector embeddings into a vector database using the following function
def get_vectorstore():

    global _vectorstore

    if _vectorstore is None:

        index = ensure_index()

        _vectorstore = PineconeVectorStore(
            index=index,
            embedding=get_embeddings(),
            namespace=settings.pinecone_namespace
        )

    return _vectorstore


# Make the vectorstore as a retriever if you want to further retrieve
def get_retriever():

    return get_vectorstore().as_retriever(
        search_kwargs={"k": settings.top_k}
    )


# If you want to add new documents in the future, call the following function
def add_documents(chunks):

    store = get_vectorstore()

    if not chunks:
        return []

    return store.add_documents(chunks)
