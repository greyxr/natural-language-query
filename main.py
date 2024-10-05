from database import *
from openai import OpenAI
import json
api_file = json.load(open('api.json'))
# openai.api_key = api_file["api_key"]

getSql = " Give me a MySQL select statement that answers the question. Only respond with mysql syntax. If there is an error do not explain it!"

def main():
    setup_db()
    #call_gpt()


def call_gpt(content):
    try:
        client = OpenAI(
            api_key=api_file["api_key"],
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            model="gpt-3.5-turbo",
        )

        return chat_completion.choices[0].message
    except:
        print('Something went wrong')

__name__
if __name__=="__main__":
    main()