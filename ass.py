import ollama

response = ollama.chat(
    stream=True,
    model='deepseek-r1:1.5b',
    messages=[
        {'role': 'user', 'content': ' what is the probability of pulling 4 ace of spades from a deck of cards?'}
    ]
)

for chunk in response:
    print(chunk['message']['content'], end='', flush=True)
# Print the response
# print(response['message']['content'])