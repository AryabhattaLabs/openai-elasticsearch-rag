import os

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )
# Model names change over time. Set OPENAI_CHAT_MODEL or OPENAI_EMBEDDING_MODEL in .env to use others.
# If you change the embedding model, recreate the index (dims) and retune BEST_SCORE_THRESHOLD.
gpt_model = os.environ.get("OPENAI_CHAT_MODEL") or "gpt-5.4-mini"
embedding_model = os.environ.get("OPENAI_EMBEDDING_MODEL") or "text-embedding-ada-002"


# INDEX_DIMENSION = 1536

def generate_embedding(text):
    print("Generating embedding for text: " + text)
    # Generate embedding using OpenAI model
    res = client.embeddings.create(input=text, model=embedding_model)
    embedding = res.data[0].embedding
    return embedding


def generate_chat_response(messages):
    # Only parameters every current chat model accepts: newer models reject max_tokens,
    # and some allow only the default temperature.
    parameters = {
        "messages": messages,
        "max_completion_tokens": 2048
    }

    parameters["model"] = gpt_model
    response = client.chat.completions.create(**parameters)

    response_text = response.choices[0].message.content
    # Replace unnecessary text
    response_text = response_text.replace("As an AI language model, ", "")
    response_text = response_text.replace("I am not capable of understanding emotions, but ", "")

    return response_text
