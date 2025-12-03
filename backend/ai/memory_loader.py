import chromadb
import os
from typing import List
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

class MemoryLoader:
    def __init__(self):
        """Initialize Memory Loader for ChromaDB"""
        # Use sentence-transformers for embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB - use in-memory for ephemeral environments (like Render)
        # Falls back to persistent storage for local development
        if os.getenv('RENDER'):
            # In-memory client for production (Render has ephemeral storage)
            self.chroma_client = chromadb.EphemeralClient()
            print("🔄 Using ChromaDB in-memory mode (ephemeral storage)")
        else:
            # Persistent client for local development
            self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
            print("💾 Using ChromaDB persistent mode (local storage)")
        
        # Collection name
        self.collection_name = "quarterly_reports"
    
    def load_past_reports(self) -> bool:
        """
        Load past reports from text file into ChromaDB
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read past reports file
            reports_file = "memory/past_reports.txt"
            if not os.path.exists(reports_file):
                raise FileNotFoundError(f"Past reports file not found: {reports_file}")
            
            with open(reports_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split content into individual quarterly reports
            reports = self._split_reports(content)
            
            if not reports:
                raise ValueError("No reports found in the file")
            
            # Delete existing collection and create new one
            try:
                self.chroma_client.delete_collection(self.collection_name)
            except:
                pass  # Collection might not exist
            
            collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Historical quarterly reports for style matching"}
            )
            
            # Generate embeddings and store reports
            embeddings = []
            documents = []
            metadatas = []
            ids = []
            
            for i, report in enumerate(reports):
                if report['text'].strip():
                    # Generate embedding
                    embedding = self._get_embedding_sync(report['text'])
                    
                    embeddings.append(embedding)
                    documents.append(report['text'])
                    metadatas.append({
                        "quarter": report['quarter'],
                        "type": "historical_report",
                        "index": i
                    })
                    ids.append(f"report_{i}_{report['quarter'].replace(' ', '_')}")
            
            # Add to collection
            if embeddings:
                collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                
                print(f"✅ Loaded {len(embeddings)} reports into ChromaDB")
                return True
            else:
                raise ValueError("No valid reports to load")
            
        except Exception as e:
            print(f"❌ Failed to load past reports: {e}")
            return False
    
    def _split_reports(self, content: str) -> List[dict]:
        """Split the content into individual quarterly reports"""
        reports = []
        
        # Split by quarters (Q1, Q2, Q3, Q4 followed by year)
        import re
        pattern = r'(Q[1-4] \d{4})'
        parts = re.split(pattern, content)
        
        current_quarter = None
        for i, part in enumerate(parts):
            if re.match(r'Q[1-4] \d{4}', part.strip()):
                current_quarter = part.strip()
            elif current_quarter and part.strip():
                # Clean up the text
                text = part.strip()
                # Remove extra whitespace and normalize
                text = re.sub(r'\n+', '\n\n', text)
                text = re.sub(r' +', ' ', text)
                
                reports.append({
                    "quarter": current_quarter,
                    "text": text
                })
        
        return reports
    
    def _get_embedding_sync(self, text: str) -> List[float]:
        """Generate embedding using SentenceTransformers (synchronous)"""
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()
    
    def get_collection_status(self) -> dict:
        """Get status of the ChromaDB collection"""
        try:
            collection = self.chroma_client.get_collection(self.collection_name)
            count = collection.count()
            return {
                "status": "ready",
                "document_count": count,
                "collection_name": self.collection_name
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "document_count": 0,
                "collection_name": self.collection_name
            }

if __name__ == "__main__":
    # Test the memory loader
    loader = MemoryLoader()
    
    print("Loading past reports into ChromaDB...")
    success = loader.load_past_reports()
    
    if success:
        status = loader.get_collection_status()
        print(f"\nCollection Status: {status}")
    else:
        print("Failed to load reports")