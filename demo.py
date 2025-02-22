import logging
import os
from deepsearcher.offline_loading import load_from_website
from deepsearcher.online_query import query
from deepsearcher.configuration import Configuration, init_config

# Suppress unnecessary logging
logging.getLogger("httpx").setLevel(logging.WARNING)

config = Configuration()
config.set_provider_config("llm", "OpenAI", {
    "base_url": "https://api.venice.ai/v1",
    "api_key": "B9Y68yQgatQw8wmpmnIMYcGip1phCt-43CS0OktZU6",
    "model": "deepseek-r1-671b"
})
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
