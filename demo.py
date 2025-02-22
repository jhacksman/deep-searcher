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
import os
from dotenv import load_dotenv
import click
import logging
from deepsearcher.offline_loading import load_from_local_files, load_from_website
from deepsearcher.online_query import query
from deepsearcher.configuration import Configuration, init_config

# Suppress unnecessary logging
logging.getLogger("httpx").setLevel(logging.WARNING)

def main():
    """Interactive demo for DeepSearcher."""
    click.echo("Welcome to DeepSearcher Interactive Demo!")
    click.echo("This demo showcases the complete DeepSearcher architecture.\n")
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize configuration
        config = Configuration()
        init_config(config)
        
        while True:
            click.echo("\n=== Data Ingestion Layer ===")
            click.echo("1. Load from website")
            click.echo("2. Load from local file")
            click.echo("3. Exit")
            
            choice = click.prompt("\nEnter choice", type=click.Choice(['1', '2', '3']))
            
            if choice == '1':
                url = click.prompt("\nEnter website URL (e.g. https://example.com)")
                if not url.startswith(("http://", "https://")):
                    click.echo("\nError: Invalid URL. Must start with http:// or https://", err=True)
                    continue
                    
                click.echo(f"\nLoading website content from {url}...")
                try:
                    load_from_website(
                        urls=url,
                        collection_name="web_content", 
                        collection_description="Website content"
                    )
                except Exception as e:
                    click.echo(f"\nError loading website: {str(e)}", err=True)
                    continue

            elif choice == '2':
                path = click.prompt("\nEnter path to local file")
                if not os.path.exists(path):
                    click.echo("\nError: File not found", err=True)
                    continue
                    
                click.echo(f"\nLoading file from {path}...")
                try:
                    load_from_local_files(
                        paths_or_directory=path,
                        collection_name="local_content",
                        collection_description="Local file content"
                    )
                except Exception as e:
                    click.echo(f"\nError loading file: {str(e)}", err=True)
                    continue

            elif choice == '3':
                click.echo("\nExiting...")
                break

            # After successful data loading, proceed with query
            click.echo("\n=== Online Serving Layer ===")
            click.echo("1. LLM breaks down query into sub-queries")
            click.echo("2. Vector database performs semantic search") 
            click.echo("3. Reflection analyzes knowledge gaps")
            click.echo("4. Final report summarizes findings")

            question = click.prompt("\nEnter your query")
            click.echo(f"\nProcessing query: {question}")
            
            try:
                result, _, consumed_token = query(question)
                click.echo("\n=== Final Report ===")
                click.echo(result)
                click.echo(f"\nTokens consumed: {consumed_token}")
            except Exception as e:
                click.echo(f"\nError processing query: {str(e)}", err=True)
    except Exception as e:
        click.echo(f"\nError: {str(e)}", err=True)
        raise

if __name__ == "__main__":
    main()
