import json
import sys
from openai import OpenAI
from database import setup_db, execute_query
from table_data.setup import TABLES

api_file = json.load(open('api.json'))

getSql = " Give me a MySQL select statement that answers the question. Only respond with mysql syntax. If there is an error do not explain it!"
create_statement = ''
for table_name in TABLES:
    create_statement += TABLES[table_name] + '\n'

cross_domain_create_statement = ''
for table_name in TABLES:
    if (table_name != 'npc'):
        cross_domain_create_statement += TABLES[table_name] + '\n'

strategies = {
    "zero_shot": create_statement + getSql,
    "single_domain_single_shot": (create_statement + 
                   "Who can I sell a weapon to within a Fighters Guild?" + 
                   "'SELECT m.MerchantName FROM merchant m INNER JOIN merchant_types mt ON m.MerchantName = mt.MerchantName WHERE m.Faction = 'Fighters Guild' AND mt.ItemType = 'Weapon';'" +
                   getSql),
    "single_domain_double_shot": (create_statement + 
                   "Who can I sell a weapon to within a Fighters Guild?" + 
                   "'SELECT m.MerchantName FROM merchant m INNER JOIN merchant_types mt ON m.MerchantName = mt.MerchantName WHERE m.Faction = 'Fighters Guild' AND mt.ItemType = 'Weapon';'" +
                                      "Who is the NPC in the Telvanni faction with the highest rank number, and what is their rank name?" + 
                   "'SELECT n.NpcName, f.RankName FROM npc n JOIN faction f ON n.Faction = f.Faction AND n.RankNumber = f.RankNumber WHERE n.Faction = 'Telvanni' ORDER BY n.RankNumber DESC LIMIT 1;'" +
                   getSql),
    "cross_domain_single_shot": (cross_domain_create_statement +
                   "Who is the NPC in the Telvanni faction with the highest rank number, and what is their rank name?" + 
                   "'SELECT n.NpcName, f.RankName FROM npc n JOIN faction f ON n.Faction = f.Faction AND n.RankNumber = f.RankNumber WHERE n.Faction = 'Telvanni' ORDER BY n.RankNumber DESC LIMIT 1;'" +
                   getSql)
}

def main():
    setup_db()
    try_strategies()

questions = [
    'Who can I sell a weapon to within a Fighters Guild?',
    'Who is the NPC in the Telvanni faction with the highest rank number, and what is their rank name?',
    'Who is the highest ranking merchant of any faction and where are they?',
    'Which NPC has the longest name, and what class are they?',
    'Which merchant has the most gold, and what do they sell?',
    'What is the rank name of the highest ranking NPC within the faction containing the least number of npcs? Who are they? What is their faction?',
    'Who are the merchants with the highest rank number, and what do they sell? What are their factions?',
    'Who is the highest ranked merchant that offers priest services? What is their rank and faction?',
    'Of the merchants that are also NPCs, which class is most common?'
    ]

failed = [
    'What is the rank name of the highest ranking NPC within the faction containing the median number of NPCS? Who are they and what is their rank name?',
    'Who is ranked highest in Telvanni?',
    'Of the merchants that are also NPCs, which class is most common?'
]

def fix_query(content, question):
    fix_statement = 'You gave this MySQL response to this question given the previous database schema. Double check the query logic, make sure the table names, attributes, and relations are correct and fix any errors and return the query in the same format. If it is already correct, return the query exactly as is here. If not, fix it and return the fixed query with the same format. Only return MySql syntax, and do not explain any errors!'
    return call_gpt(create_statement + ' ' + fix_statement + ' Question:' + question + ' ' + content)

def try_strategies():
    try:
        orig_stdout = sys.stdout
        f = open('out.txt', 'w')
        sys.stdout = f
        for strategy in strategies:
            for question in questions:
                content = strategies[strategy] + " Question: " + question
                response = call_gpt(content)
                if (response is None):
                    print('An error occurred.')
                    break
                fixed_response = fix_query(response, question)
                # Replace chatgpt characters
                fixed_response = fixed_response.replace('`','').replace("mysql", '').replace("sql", '')
                database_response = execute_query(fixed_response)
                friendly_response = get_friendly_response(question, database_response)
                print_response(strategy, question, content, response, fixed_response, database_response, friendly_response)
    except:
        print('An error occurred.')
    finally:
        sys.stdout = orig_stdout
        f.close()

def print_response(strategy, question, content, response, fixed_response, database_response, friendly_response):
    print('---------------------------------------------------------\nStrategy: ' + strategy)
    print(question + '\n')
    print('---------\nContent:\n' + content)
    print('---------\nInitial Response:\n' + response)
    print('---------\nFixed Response:\n' + fixed_response)
    print('---------\nRaw database response:\n' + str(database_response))
    print('---------\nFriendly response:\n' + friendly_response + '\n---------')    

def get_friendly_response(question, result):
    friendly_response = 'This database response answers this question. Please use this response to answer the question.'
    return call_gpt(friendly_response + ' Question: ' + question + ' Response: ' + str(result))

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
            model="gpt-4o",
        )

        return chat_completion.choices[0].message.content
    except:
        print('Something went wrong')

__name__
if __name__=="__main__":
    main()