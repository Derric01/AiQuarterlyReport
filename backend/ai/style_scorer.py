import chromadb
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

class StyleScorer:
    def __init__(self):
        """Initialize Style Scorer with ChromaDB and SentenceTransformers"""
        # Use sentence-transformers for embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        
        try:
            # Try to get existing collection
            self.collection = self.chroma_client.get_collection("quarterly_reports")
        except:
            # Create collection if it doesn't exist
            self.collection = self.chroma_client.create_collection(
                name="quarterly_reports",
                metadata={"description": "Historical quarterly reports for style matching"}
            )
    
    async def score(self, report: str) -> Dict[str, Any]:
        """
        Calculate style similarity score using RAG
        
        Args:
            report: Generated report text
            
        Returns:
            dict: Style score and retrieved similar reports
        """
        try:
            # Generate embedding for the input report
            report_embedding = await self._get_embedding(report)
            
            # Query similar reports from vector database
            similar_reports = self._query_similar_reports(report_embedding, n_results=3)
            
            # Calculate average similarity score
            if similar_reports and len(similar_reports['distances'][0]) > 0:
                # ChromaDB returns distances (lower = more similar), convert to similarity score
                distances = similar_reports['distances'][0]
                similarities = [max(0, 1 - distance) for distance in distances]
                avg_similarity = sum(similarities) / len(similarities)
                score = avg_similarity * 100  # Convert to percentage
                
                # Prepare retrieved documents
                retrieved_docs = []
                if similar_reports['documents']:
                    for i, doc in enumerate(similar_reports['documents'][0]):
                        retrieved_docs.append({
                            "text": doc,
                            "similarity": similarities[i] if i < len(similarities) else 0,
                            "metadata": similar_reports['metadatas'][0][i] if similar_reports['metadatas'] and i < len(similar_reports['metadatas'][0]) else {}
                        })
            else:
                score = 0
                retrieved_docs = []
            
            return {
                "score": min(100, max(0, score)),  # Ensure score is between 0-100
                "retrieved": retrieved_docs,
                "method": "SentenceTransformers embeddings with cosine similarity",
                "total_references": len(retrieved_docs)
            }
            
        except Exception as e:
            return {
                "score": 0,
                "retrieved": [],
                "error": f"Style scoring failed: {str(e)}",
                "method": "SentenceTransformers embeddings with cosine similarity",
                "total_references": 0
            }
    
    async def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding using SentenceTransformers"""
        try:
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")
    
    def _query_similar_reports(self, embedding: List[float], n_results: int = 3) -> Dict:
        """Query ChromaDB for similar reports"""
        try:
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Query error: {e}")
            return {"documents": [], "distances": [], "metadatas": []}
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the ChromaDB collection"""
        try:
            count = self.collection.count()
            return {
                "collection_name": "quarterly_reports",
                "document_count": count,
                "status": "ready"
            }
        except Exception as e:
            return {
                "collection_name": "quarterly_reports",
                "document_count": 0,
                "status": f"error: {str(e)}"
            }

# Synchronous wrapper
class SyncStyleScorer(StyleScorer):
    def score_sync(self, report: str) -> Dict[str, Any]:
        """Synchronous version of score method"""
        try:
            # Generate embedding for the input report
            report_embedding = self._get_embedding_sync(report)
            
            # Query similar reports from vector database
            similar_reports = self._query_similar_reports(report_embedding, n_results=3)
            
            # Calculate average similarity score
            if similar_reports and len(similar_reports['distances'][0]) > 0:
                distances = similar_reports['distances'][0]
                similarities = [max(0, 1 - distance) for distance in distances]
                avg_similarity = sum(similarities) / len(similarities)
                score = avg_similarity * 100
                
                # Prepare retrieved documents
                retrieved_docs = []
                if similar_reports['documents']:
                    for i, doc in enumerate(similar_reports['documents'][0]):
                        retrieved_docs.append({
                            "text": doc,
                            "similarity": similarities[i] if i < len(similarities) else 0,
                            "metadata": similar_reports['metadatas'][0][i] if similar_reports['metadatas'] and i < len(similar_reports['metadatas'][0]) else {}
                        })
            else:
                score = 0
                retrieved_docs = []
            
            return {
                "score": min(100, max(0, score)),
                "retrieved": retrieved_docs,
                "method": "OpenAI embeddings with cosine similarity",
                "total_references": len(retrieved_docs)
            }
            
        except Exception as e:
            return {
                "score": 0,
                "retrieved": [],
                "error": f"Style scoring failed: {str(e)}",
                "method": "OpenAI embeddings with cosine similarity", 
                "total_references": 0
            }
    
    def _get_embedding_sync(self, text: str) -> List[float]:
        """Generate embedding using SentenceTransformers (synchronous)"""
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()

if __name__ == "__main__":
    # Test the style scorer
    scorer = SyncStyleScorer()
    
    # Print collection info
    info = scorer.get_collection_info()
    print(f"Collection info: {info}")
    
    # Test scoring
    test_report = "The MSCI ACWI gained 8.2% this quarter. The S&P 500 returned 10.6%."
    
    try:
        result = scorer.score_sync(test_report)
        print("\nStyle Score Result:")
        print(f"Score: {result['score']}")
        print(f"Retrieved: {len(result['retrieved'])} documents")
    except Exception as e:
        print(f"Error: {e}")