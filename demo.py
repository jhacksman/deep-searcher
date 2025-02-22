import os
# Disable tokenizer parallelism to avoid deadlocks
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import click
from dotenv import load_dotenv
from deepsearcher.configuration import Configuration, init_config
from deepsearcher.offline_loading import load_from_website
from deepsearcher.online_query import query

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
            click.echo("2. Exit")
            
            choice = click.prompt("\nEnter choice", type=click.Choice(['1', '2']))
            
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
                    
            elif choice == '2':
                click.echo("\nExiting...")
                break
    except Exception as e:
        click.echo(f"\nError: {str(e)}", err=True)
        raise

if __name__ == "__main__":
    main()
