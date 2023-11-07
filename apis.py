import requests
from credentials import GPT_TOKEN


def get_random_duck():
    endpoint = 'https://random-d.uk/api/random'
    response = requests.get(endpoint)
    data = response.json()
    return data['url']


def ask_chat_gpt(question):

  url = 'https://api.openai.com/v1/chat/completions'
  headers = {
              'Content-Type': 'application/json',
              'Authorization': f'Bearer {GPT_TOKEN}'
            }
  data = {
          'model': 'gpt-3.5-turbo',
          'messages': [{'role': 'user', 'content': question}]
          }
  response = requests.post(url,json=data,headers=headers)
  data = response.json()
  print(data)
  return data['choices'][0]['message']['content']

