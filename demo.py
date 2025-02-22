"""
DeepSearcher Demo

This demo showcases the complete DeepSearcher architecture:
1. Data Ingestion Layer
   - Local files (PDF, MD, TXT)
   - Web pages via FireCrawl
2. Online Serving Layer  
   - LLM query breakdown
   - Vector database search
   - Semantic search
   - Reflection loop
   - Final report generation
"""
import logging
from deepsearcher.offline_loading import load_from_local_files, load_from_website
from deepsearcher.online_query import query
from deepsearcher.configuration import Configuration, init_config

# Suppress unnecessary logging
logging.getLogger("httpx").setLevel(logging.WARNING)

def main():
    # Initialize configuration
    config = Configuration()
    init_config(config=config)

    print("\n=== Data Ingestion Layer ===")
    
    # Load website content
    print("\nLoading website content...")
    load_from_website(
        urls="https://example.com",
        collection_name="web_content",
        collection_description="Example website content"
    )

    print("\n=== Online Serving Layer ===")
    print("1. LLM breaks down query into sub-queries")
    print("2. Vector database performs semantic search")
    print("3. Reflection analyzes knowledge gaps")
    print("4. Final report summarizes findings")
    
    # Example query that will trigger reflection
    question = "Compare the architecture and performance of Milvus with other vector databases. Include specific metrics and use cases."
    
    print(f"\nQuery: {question}")
    result, _, consumed_token = query(question)
    
    print("\n=== Final Report ===")
    print(result)
    print(f"\nTokens consumed: {consumed_token}")

if __name__ == "__main__":
    main()
