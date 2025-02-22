import logging
from deepsearcher.offline_loading import load_from_website
from deepsearcher.online_query import query
from deepsearcher.configuration import Configuration, init_config

# Suppress unnecessary logging
logging.getLogger("httpx").setLevel(logging.WARNING)

config = Configuration()  # Use default configuration
init_config(config=config)

# Load data from example.com
website_url = "https://example.com"
load_from_website(
    urls=website_url,
    collection_name="example",
    collection_description="Example website content"
)

# Query example
question = "What topics are discussed in the loaded content?"
result, _, consumed_token = query(question)
print(f"\nAnswer:\n{result}\n")
print(f"Consumed tokens: {consumed_token}")
