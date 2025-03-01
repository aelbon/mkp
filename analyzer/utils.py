import openai
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
import json


with open('./data/llm_data.json', 'r') as f:
    llm_data = {item['name']: {k: v for k, v in item.items() if k != 'name'} for item in json.load(f)}


def bot_completion(prompt, model="gpt-3.5-turbo-0125", temperature=1.0):
    client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"))
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model=model,
    temperature=temperature,
    )
    llm_pricing = llm_data[model]
    usage = chat_completion.usage
    input = usage.prompt_tokens
    output = usage.completion_tokens
    cost = llm_pricing['inputPrice'] * input / 1000 + (llm_pricing['outputPrice'] * output / 1000)
    content = chat_completion.choices[0].message.content
    return content, cost
