import openai

def Connection(GPTCredentials: dict):
    # Connect to openai to later make consults
    openai.api_key = GPTCredentials["token"]
    return openai