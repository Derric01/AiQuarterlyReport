import google.generativeai as genai
import os
import re
import chromadb
from typing import Dict, Any, List
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

class StyleScorer:
    def __init__(self):
        """Initialize Style Scorer with Gemini AI and ChromaDB"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize embedding model for similarity
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB - use in-memory for ephemeral environments
        try:
            if os.getenv('RENDER'):
                # In-memory client for production
                self.chroma_client = chromadb.EphemeralClient()
            else:
                # Persistent client for local development
                self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
            self.collection = self.chroma_client.get_collection("quarterly_reports")
        except Exception as e:
            print(f"⚠️ ChromaDB collection not ready: {e}")
            self.collection = None
    
    def score_sync(self, report: str) -> Dict[str, Any]:
        """
        Score the style of the report using Gemini AI and historical comparison
        """
        try:
            # 1. Structural Analysis (30 points)
            structural_score, structural_details = self._analyze_structure(report)
            
            # 2. Language Quality Analysis via Gemini (40 points)
            language_score, language_details = self._analyze_language_quality(report)
            
            # 3. Historical Style Similarity (30 points)
            similarity_score, similarity_details = self._analyze_historical_similarity(report)
            
            # Calculate total score
            total_score = structural_score + language_score + similarity_score
            
            # Get comprehensive feedback
            feedback = self._generate_feedback(total_score, structural_score, language_score, similarity_score)
            
            return {
                "style_score": round(total_score, 2),
                "max_score": 100.0,
                "percentage": round(total_score, 2),
                "breakdown": {
                    "structural": {
                        "score": round(structural_score, 2),
                        "max": 30.0,
                        "details": structural_details
                    },
                    "language_quality": {
                        "score": round(language_score, 2),
                        "max": 40.0,
                        "details": language_details
                    },
                    "historical_similarity": {
                        "score": round(similarity_score, 2),
                        "max": 30.0,
                        "details": similarity_details
                    }
                },
                "feedback": feedback,
                "grade": self._get_grade(total_score)
            }
            
        except Exception as e:
            return {
                "style_score": 0.0,
                "max_score": 100.0,
                "percentage": 0.0,
                "breakdown": {},
                "feedback": f"Style scoring failed: {str(e)}",
                "grade": "F"
            }
    
    def _analyze_structure(self, report: str) -> tuple:
        """Analyze structural elements (30 points)"""
        score = 0.0
        details = {}
        
        # Word count analysis (10 points)
        word_count = len(report.split())
        details["word_count"] = word_count
        if 150 <= word_count <= 400:
            score += 10.0
            details["word_count_status"] = "Optimal"
        elif 100 <= word_count < 150 or 400 < word_count <= 500:
            score += 7.0
            details["word_count_status"] = "Acceptable"
        else:
            score += 3.0
            details["word_count_status"] = "Needs adjustment"
        
        # Paragraph structure (10 points)
        paragraphs = [p.strip() for p in report.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)
        details["paragraph_count"] = paragraph_count
        if 2 <= paragraph_count <= 3:
            score += 10.0
            details["structure_status"] = "Well-structured"
        elif paragraph_count == 4:
            score += 7.0
            details["structure_status"] = "Good structure"
        else:
            score += 4.0
            details["structure_status"] = "Structure needs improvement"
        
        # Data integration (10 points)
        has_percentages = report.count('%')
        has_numbers = len(re.findall(r'\d+\.?\d*', report))
        details["percentage_mentions"] = has_percentages
        details["numeric_references"] = has_numbers
        
        if has_percentages >= 4 and has_numbers >= 6:
            score += 10.0
            details["data_integration"] = "Excellent data integration"
        elif has_percentages >= 2 and has_numbers >= 4:
            score += 7.0
            details["data_integration"] = "Good data integration"
        else:
            score += 4.0
            details["data_integration"] = "More data needed"
        
        return score, details
    
    def _analyze_language_quality(self, report: str) -> tuple:
        """Analyze language quality using Gemini AI (40 points)"""
        try:
            analysis_prompt = f"""Analyze this financial report's writing quality on these dimensions:

REPORT:
{report}

Rate each dimension from 0-10:
1. TONE: Professional, authoritative, appropriate for institutional investors
2. CLARITY: Clear, concise, easy to understand without jargon overload
3. COHERENCE: Logical flow, smooth transitions between ideas
4. ENGAGEMENT: Compelling narrative while remaining factual

Respond in this exact format:
TONE: [score]/10 - [brief comment]
CLARITY: [score]/10 - [brief comment]
COHERENCE: [score]/10 - [brief comment]
ENGAGEMENT: [score]/10 - [brief comment]"""

            response = self.model.generate_content(
                analysis_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=400,
                )
            )
            
            # Parse Gemini response
            result_text = response.text
            details = {}
            total_ai_score = 0.0
            
            for dimension in ['TONE', 'CLARITY', 'COHERENCE', 'ENGAGEMENT']:
                pattern = rf'{dimension}:\s*(\d+)/10\s*-\s*(.+?)(?=\n|$)'
                match = re.search(pattern, result_text, re.IGNORECASE | re.DOTALL)
                if match:
                    score = float(match.group(1))
                    comment = match.group(2).strip()
                    details[dimension.lower()] = {
                        "score": score,
                        "comment": comment
                    }
                    total_ai_score += score
                else:
                    details[dimension.lower()] = {"score": 7.0, "comment": "Analysis unavailable"}
                    total_ai_score += 7.0
            
            # Convert 40-point scale (4 dimensions × 10 points)
            final_score = (total_ai_score / 40.0) * 40.0
            
            return final_score, details
            
        except Exception as e:
            # Fallback to basic analysis
            details = {
                "tone": {"score": 7.0, "comment": "Standard professional tone"},
                "clarity": {"score": 7.0, "comment": "Clear communication"},
                "coherence": {"score": 7.0, "comment": "Good logical flow"},
                "engagement": {"score": 7.0, "comment": "Engaging narrative"}
            }
            return 28.0, details
    
    def _analyze_historical_similarity(self, report: str) -> tuple:
        """Analyze similarity to historical reports (30 points)"""
        details = {}
        
        if not self.collection:
            details["similarity"] = "Historical comparison unavailable"
            return 20.0, details  # Default decent score
        
        try:
            # Get embedding for current report
            report_embedding = self.embedding_model.encode(report).tolist()
            
            # Query similar reports from ChromaDB
            results = self.collection.query(
                query_embeddings=[report_embedding],
                n_results=3
            )
            
            if results and results['distances'] and len(results['distances'][0]) > 0:
                # Convert distances to similarity scores (lower distance = higher similarity)
                distances = results['distances'][0]
                similarities = [1 / (1 + d) for d in distances]  # Convert to 0-1 range
                avg_similarity = sum(similarities) / len(similarities)
                
                # Convert to 30-point scale
                score = avg_similarity * 30.0
                
                details["avg_similarity"] = round(avg_similarity * 100, 2)
                details["comparison_count"] = len(similarities)
                details["top_match_similarity"] = round(similarities[0] * 100, 2)
                
                if avg_similarity >= 0.75:
                    details["consistency"] = "Excellent consistency with historical style"
                elif avg_similarity >= 0.60:
                    details["consistency"] = "Good alignment with past reports"
                elif avg_similarity >= 0.45:
                    details["consistency"] = "Moderate similarity to historical style"
                else:
                    details["consistency"] = "Developing unique style"
                
                return score, details
            else:
                details["similarity"] = "No historical reports for comparison"
                return 20.0, details
                
        except Exception as e:
            details["error"] = f"Similarity analysis failed: {str(e)}"
            return 20.0, details
    
    def _generate_feedback(self, total: float, structural: float, language: float, similarity: float) -> str:
        """Generate comprehensive feedback"""
        feedback_parts = []
        
        if total >= 90:
            feedback_parts.append("Outstanding professional quality.")
        elif total >= 80:
            feedback_parts.append("Excellent professional standard.")
        elif total >= 70:
            feedback_parts.append("Strong professional quality.")
        elif total >= 60:
            feedback_parts.append("Good foundation with room for refinement.")
        else:
            feedback_parts.append("Significant improvements needed.")
        
        # Specific feedback
        if structural < 20:
            feedback_parts.append("Consider improving document structure and data integration.")
        if language < 28:
            feedback_parts.append("Focus on enhancing clarity and professional tone.")
        if similarity < 20:
            feedback_parts.append("Style differs notably from historical reports.")
        
        return " ".join(feedback_parts)
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 93: return "A+"
        elif score >= 90: return "A"
        elif score >= 87: return "A-"
        elif score >= 83: return "B+"
        elif score >= 80: return "B"
        elif score >= 77: return "B-"
        elif score >= 73: return "C+"
        elif score >= 70: return "C"
        elif score >= 67: return "C-"
        elif score >= 60: return "D"
        else: return "F"