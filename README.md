# Normal Language Query Test Script

## Description

This project tests out different NLQ strategies for generating responses from a MySQL database. It uses four tables populated with data about NPCs from the 2002 game <i>The Elder Scrolls 3: Morrowind</i>.

## Database Schema
<img src=./schema.png>

## Sample Questions
### Successful Question
<b>Question:</b>

Which NPC has the longest name, and what class are they?

<b>Query:</b>

```SELECT NpcName, Class FROM npc ORDER BY CHAR_LENGTH(NpcName) DESC LIMIT 1;```

<b>Response</b>:

The NPC with the longest name is "Morning-Star-Steals-Away-Clouds," and their class is "Slave."

### Failed Question
<b>Question:</b>

Who can I sell a weapon to within a Fighters Guild?

<b>Query:</b>

```SELECT m.MerchantName FROM merchant m INNER JOIN merchant_types mt ON m.MerchantName = mt.MerchantName WHERE m.Faction = 'Fighters Guild';```

<b>Response</b>:

The issue with the response to this question is that the query wasn't filtering by what the merchant sells, only by what faction the merchant was a part of. I fixed this by using a corrected SQL query as part of the single and double shots. The zero-shot query also fixed itself as I upgraded the chat model to chatgpt-4o.

### Strategies and Differences
I used zero shot, single domain single shot, single domain double shot, and cross-domain single shot strategies in my testing. I found that the model had better success on the single and double shot strategies, but that gap narrowed and closed as I upgraded the chat gpt model I was using (I went from chatgpt-3.5-turbo to chatgpt-4o). No matter the strategy I used, the model had a hard time differentating between when NPC IDs should be used vs NPC names. A lot of my issues had to do with my column names, which could be ambiguous depending on the question context. I imported my data and tables directly from data obtained from Morrowind itself. If I were to continue working on this, I would re-do the tables to be better suited to the model and make the columns more descriptive.

I was also having problems with the zero and single shot models wanting to make extraneous joins on the table. I fixed that by making an interim chatgpt call, passing it the schema, question, and response again and asking it to fix any errors it found. This reduced the syntax errors from the zero and single shot models to almost none, but only after paring down the request. When I put too much into the interim request, it would get confused and introduce errors instead of fixing them.

I accomplished my cross-domain single shot strategy by removing a table from the schema and asking questions about that table, passing it sample queries using schema I passed it. It didn't do noticeably worse on those questions compared against questions that didn't use that table.
