from database import *
from openai import OpenAI
import json
api_file = json.load(open('api.json'))
# openai.api_key = api_file["api_key"]

def main():
    setup_db()
    #call_gpt()


def call_gpt():
    try:
        client = OpenAI(
            # This is the default and can be omitted
            api_key=api_file["api_key"],
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model="gpt-3.5-turbo",
        )

        print(chat_completion.choices[0].message)
    except:
        print('Something went wrong')

__name__
if __name__=="__main__":
    main()