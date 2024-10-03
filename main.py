from database import *
from openai import OpenAI

def main():
    create_database()
    create_tables()


def call_gpt():
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
        ]
    )

# __name__
if __name__=="__main__":
    main()