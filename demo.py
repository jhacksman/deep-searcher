import logging
import os
from deepsearcher.offline_loading import load_from_website, load_from_local_files
from deepsearcher.online_query import query
from deepsearcher.configuration import Configuration, init_config

# Suppress unnecessary logging
logging.getLogger("httpx").setLevel(logging.WARNING)

def main():
    # Initialize configuration with venice.ai settings
    config = Configuration()
    config.set_provider_config("llm", "OpenAI", {
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.venice.ai/api/v1"),
        "model": os.getenv("OPENAI_MODEL", "deepseek-r1-671b")
    })
    init_config(config)

    # Load data (uncomment and modify as needed)
    # From website:
    # website_url = "https://example.com"
    # load_from_website(
    #     urls=website_url,
    #     collection_name="example",
    #     collection_description="Example website content"
    # )

    # From local file:
    # load_from_local_files(
    #     paths_or_directory="path/to/file",
    #     collection_name="local",
    #     collection_description="Local content"
    # )

    # Query example
    question = "What topics are discussed in the loaded content?"
    result, _, tokens = query(question)
    print(f"\nAnswer:\n{result}\n")
    print(f"Tokens used: {tokens}")

if __name__ == "__main__":
    main()
