import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings

class VectorService:
    def __init__(self):
        # 1. Initialize the ChromaDB client (it saves data to your VECTOR_DB_PATH)
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        
        # 2. Use Ollama for Embeddings (so it's free!)
        self.emb_fn = embedding_functions.OllamaEmbeddingFunction(
            url="http://localhost:11434/api/embeddings",
            model_name="llama3" 
        )
        
        # 3. Get or create a "Collection" (like a table in a database)
        self.collection = self.client.get_or_create_collection(
            name="pdf_knowledge",
            embedding_function=self.emb_fn
        )

    async def add_text_to_index(self, text: str, filename: str, user_id: str):
        chunks = [text[i:i + 500] for i in range(0, len(text), 500)]
        ids = [f"{user_id}_{filename}_{i}" for i in range(len(chunks))]
        
        # Store user_id in metadata so we can filter by it later
        metadatas = [{"user_id": user_id, "source": filename} for _ in range(len(chunks))]
    
        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        return len(chunks)




    

    async def search_docs(self, query: str, user_id: str, n_results: int = 3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"user_id": user_id}  # THIS IS THE KEY: Filter by user!
        )
        
        if not results['documents'] or not results['documents'][0]:
            return "No relevant documents found for this user."
            
        return "\n---\n".join(results['documents'][0])

vector_service = VectorService()