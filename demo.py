import os
import click
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from deepsearcher.configuration import Configuration, init_config
from deepsearcher.offline_loading import load_from_local_files, load_from_website
from deepsearcher.online_query import query

# Constants
DEFAULT_BASE_URL = "https://api.venice.ai/api/v1"
DEFAULT_MODEL = "deepseek-r1-671b"
DEFAULT_DB_PATH = "./milvus.db"

def confirm_env_var(var_name: str, default: str = None, hide_input: bool = False) -> str:
    """Confirm or prompt for an environment variable."""
    current_value = os.getenv(var_name)
    
    if current_value:
        # Show found value and confirm
        display_value = '*' * 8 if hide_input else current_value
        click.echo(f"Found {var_name} in environment: {display_value}")
        if not click.confirm("Is this correct? [Y/n]", default=True):
            current_value = click.prompt(
                f"Please enter new value for {var_name}",
                default=default,
                hide_input=hide_input
            )
    else:
        # Prompt for missing value
        click.echo(f"Could not find {var_name} in .env file or environment")
        current_value = click.prompt(
            f"Please enter value for {var_name}",
            default=default,
            hide_input=hide_input,
            prompt_suffix=": "  # Cleaner prompt format
        )
    
    return current_value

def setup_env_vars():
    """Set up environment variables, checking .env first."""
    load_dotenv()
    
    # OpenAI base URL
    os.environ["OPENAI_BASE_URL"] = confirm_env_var(
        "OPENAI_BASE_URL",
        default=DEFAULT_BASE_URL
    )
    
    # OpenAI API key
    os.environ["OPENAI_API_KEY"] = confirm_env_var(
        "OPENAI_API_KEY",
        hide_input=True
    )
    
    # Model name
    os.environ["OPENAI_MODEL"] = confirm_env_var(
        "OPENAI_MODEL",
        default=DEFAULT_MODEL
    )

def setup_milvus():
    """Configure Milvus with local database."""
    config = Configuration()
    
    # Check if DB_PATH exists in .env
    db_path = confirm_env_var("DB_PATH", default=DEFAULT_DB_PATH)
    
    # Ensure directory exists
    db_dir = os.path.dirname(os.path.abspath(db_path))
    os.makedirs(db_dir, exist_ok=True)
    
    config.set_provider_config(
        "vector_db",
        "Milvus",
        {
            "uri": db_path,
            "default_collection": "deepsearcher",
            "token": "root:Milvus",
            "db": "default"
        }
    )
    return config

def load_data():
    """Prompt for and load data."""
    load_type = click.prompt(
        "Load from (1) local file or (2) website URL?",
        type=click.Choice(['1', '2'])
    )
    
    if load_type == '1':
        path = click.prompt("Enter path to local file")
        load_from_local_files(paths_or_directory=path)
    else:
        url = click.prompt("Enter website URL")
        load_from_website(urls=url)

def main():
    """Interactive demo for DeepSearcher."""
    click.echo("Welcome to DeepSearcher Interactive Demo!")
    click.echo("This demo will guide you through the setup and query process.\n")
    
    try:
        # Setup environment
        click.echo("Step 1: Configure OpenAI API")
        setup_env_vars()
        
        # Configure Milvus
        click.echo("\nStep 2: Configure local database")
        config = setup_milvus()
        init_config(config)
        
        # Load data
        click.echo("\nStep 3: Load data")
        load_data()
        
        # Get question
        click.echo("\nStep 4: Ask a question")
        question = click.prompt("Enter your question")
        
        # Query and display result
        click.echo("\nProcessing query...")
        result = query(question)
        click.echo("\nResult:")
        click.echo(result)
        
    except Exception as e:
        click.echo(f"\nError: {str(e)}", err=True)
        raise

if __name__ == "__main__":
    main()
