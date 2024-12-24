# importing the requests library
import requests
from datetime import datetime
# api-endpoint
URL = "https://tst.api.itaap.philips.com/philips-ai-modelserving-api/v1/ai/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-01"

payload = {
    "messages": [
        {
            "content": "What are the key attractions in the city of Delhi? Please describe in details.",
            "role": "user"
        }
    ],
    "max_tokens": 4096,
    "n": 1,
    "stream": False,
    "temperature": 0.0
}

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Inp4ZWcyV09OcFRrd041R21lWWN1VGR0QzZKMCIsImtpZCI6Inp4ZWcyV09OcFRrd041R21lWWN1VGR0QzZKMCJ9.eyJhdWQiOiJhcGk6Ly9waGlsaXBzLWFpLW1vZGVsLXNlcnZpbmctYXBpLW5vbi1wcm9kIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvMWE0MDdhMmQtNzY3NS00ZDE3LTg2OTItYjNhYzI4NTMwNmU0LyIsImlhdCI6MTczMjU1MzE1NCwibmJmIjoxNzMyNTUzMTU0LCJleHAiOjE3MzI1NTcwNTQsImFpbyI6ImsyQmdZSWl4V2J6VllJOEVwMTh1bndhWDhnTWpBQT09IiwiYXBwaWQiOiI3OTk4YjgyMy1kYmFjLTQ2YmItODdmMy00NWQ5ZjNhNjU3NmMiLCJhcHBpZGFjciI6IjEiLCJpZHAiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8xYTQwN2EyZC03Njc1LTRkMTctODY5Mi1iM2FjMjg1MzA2ZTQvIiwib2lkIjoiNTZmYWIzNGMtNDk2Yi00N2E1LWFmODgtMjc2NWE4MjZlMmRjIiwicmgiOiIxLkFRa0FMWHBBR25WMkYwMkdrck9zS0ZNRzVFbng5Z2E5MGhKR25GeGlQeXpRc1VrSkFBQUpBQS4iLCJyb2xlcyI6WyJwb3N0LmFpbW9kZWxzZXJ2ZSJdLCJzdWIiOiI1NmZhYjM0Yy00OTZiLTQ3YTUtYWY4OC0yNzY1YTgyNmUyZGMiLCJ0aWQiOiIxYTQwN2EyZC03Njc1LTRkMTctODY5Mi1iM2FjMjg1MzA2ZTQiLCJ1dGkiOiJMakQ3N0FsZVNrYVpFbzJLdzZvS0FBIiwidmVyIjoiMS4wIn0.naAWwSmpIzMjyac3YyxdkepNurhT3klS2KrAfKzh0JEkiQBzMmTLOpTA-OQK50JfgonNcjBON_l_DsaB9kjmtaSd-OXZBnJStwa5jMKsnLR1AA53Y3YEmK2TP0cbdrfDkinGdp2pNieFjzjOZS6XuB8ou85shytm2xjciG6NTj40pqfbHfGnNZklVVO6CguXxOJxDpZmK9ElAkgnYy2N085DEgB67Pxa6AAo02izb4s_O8RBozX_nUzUykHtJIU7LHgmcbWV_mM7qL1u_TQNlakCz9saluKe98v5qVIE0llcPeijUIlNOsuO7sN6NxPzw3bwvfrXaoHefxcxHmwzug";
token = "Bearer " + token;

headers = {
    "Authorization":  token,
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
