import aiohttp
from credentials import GPT_TOKEN


async def get_random_duck():
    endpoint = 'https://random-d.uk/api/random'
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as response:
            data = await response.json()
            return data['url']

async def ask_chat_gpt(question):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {GPT_TOKEN}'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': question}]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            data = await response.json()
            return data['choices'][0]['message']['content']

