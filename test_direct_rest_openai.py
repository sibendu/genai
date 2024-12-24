# importing the requests library
import requests
from datetime import datetime
# api-endpoint
URL = "https://it-dce-openai-assistant-useast2.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2023-07-01-preview"

payload = {
 "messages": [
  {
   "role": "system",
   "content": "you are a helpful travel assistant"
  },
  {
   "role": "user",
   "content": "What are the key attractions in the city of Delhi? Please describe in details."
  }
 ],
 "stream": True
}

api_key = "4c47958493254eccba0c480c2f8de157";

headers = {
    "api-key":  api_key,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# sending get request and saving the response as response object
#r = requests.post(url = URL, headers = headers, json = payload)

# extracting data in json format
#print(r)
#print(r.json())

print('Time at start: '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
with requests.post(URL, headers = headers, json=payload) as response:
    # Raise an exception for HTTP errors
    response.raise_for_status()

    # Iterate through the response line by line
    for line in response.iter_lines():
        # Decode and process each line of the response
        if line:
            print('Time now: '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            decoded_line = line.decode('utf-8')
            print(decoded_line)
