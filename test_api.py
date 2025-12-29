from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": "Hi, I'm just testing your API"
    }]
)

print(resp.output[0].content[0].text)