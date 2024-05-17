from dotenv import load_dotenv
from openai import OpenAI
import tiktoken

load_dotenv('.env')

model_default = "gpt-4o"

client = OpenAI()

# This is the "Updated" helper function for calling LLM
def get_completion(prompt, model=model_default, temperature=0, top_p=1.0, max_tokens=1024, n=1):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1,
        # response_format={ "type": "json_object" },
    )
    return response.choices[0].message.content


# This a "modified" helper function that we will discuss in this session
# Note that this function directly take in "messages" as the parameter.
def get_completion_from_messages(messages, model=model_default, temperature=0, top_p=1.0, max_tokens=1024, n=1):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1,
        # response_format={ "type": "json_object" },
    )
    return response.choices[0].message.content


# This function is for calculating the tokens given the "messages"
# ⚠️ This is simplified implementation that is good enough for a rough estimation
# For accurate estimation of the token counts, please refer to the "Extra" at the bottom of this notebook
def num_tokens_from_message_rough(messages):
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    value = ' '.join([x.get('content') for x in messages])
    return len(encoding.encode(value))


def get_embedding(input, model='text-embedding-3-small'):
    response = client.embeddings.create(
        input=input,
        model=model
    )
    return [x.embedding for x in response.data]


