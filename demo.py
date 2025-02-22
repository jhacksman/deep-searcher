import logging
import os
from deepsearcher.offline_loading import load_from_website
from deepsearcher.online_query import query
from deepsearcher.configuration import Configuration, init_config

# Suppress unnecessary logging
logging.getLogger("httpx").setLevel(logging.WARNING)

config = Configuration()  # Customize your config here
init_config(config=config)

# Load data from local file
load_from_local_files(
    paths_or_directory="examples/data/WhatisMilvus.pdf",
    collection_name="milvus_docs",
    collection_description="All Milvus Documents"
)

# Query example
question = "What topics are discussed in the loaded content?"
result, _, consumed_token = query(question)
print(f"\nAnswer:\n{result}\n")
print(f"Consumed tokens: {consumed_token}")
