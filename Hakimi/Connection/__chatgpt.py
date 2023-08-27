import openai

def Connection(GPTCredentials: dict) -> openai:

    return openai(api_key = GPTCredentials['token'])