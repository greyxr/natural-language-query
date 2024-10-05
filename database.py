import mysql.connector
from mysql.connector import errorcode
from setup import TABLES
import json
from table_data.factions import insert_factions
from table_data.npcs import insert_npcs
db_file = 'db.json'
db_name = 'morrowind_tables'

def connect_to_db():
  try:
      data = json.load(open(db_file))
      conn = mysql.connector.connect(user=data["user"],
                                password=data["password"],
                                host=data["host"],
                                database=data["database"])
      return conn
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)

def execute_query(query):
    conn = connect_to_db()
    if conn and conn.is_connected():
        with conn.cursor() as cursor:
            result = cursor.execute(query)
            rows = cursor.fetchall()
            for rows in rows:
                print(rows)
        cursor.close()
        conn.close()
    else:
        print("Could not connect")

def create_tables():
  conn = connect_to_db()
  if conn and conn.is_connected():
   for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        conn.cursor().execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
  else:
    print("Couldn't connect to DB")
  conn.cursor().close()
  conn.close()

def create_database():
      try:
        data = json.load(open(db_file))
        conn = mysql.connector.connect(user=data["user"],
                                password=data["password"],
                                host=data["host"],
                                )
        db_name = data["database"]
        print('Dropping database {}: '.format(db_name), end='')
        conn.cursor().execute('DROP DATABASE IF EXISTS ' + db_name)
        print('OK')
        print('Creating database {}: '.format(db_name), end='')
        conn.cursor().execute('CREATE DATABASE ' + db_name)
        print('OK')
        conn.cursor().close()
        conn.close()
      except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
          print("Database does not exist")
        else:
          print(err)
          
def load_values():
  load_factions()
  load_merchants()
  load_merchant_types()
  load_npcs()


from table_data.merchant_type import insert_merchants as insert_merchant_type_statement
def load_merchant_types():
    conn = connect_to_db()
    if conn and conn.is_connected():
      table_name = 'merchant_types'
      try:
          print("Loading data for table {}: ".format(table_name), end='')
          cursor = conn.cursor()
          for statement in insert_merchant_type_statement:
            cursor.execute(statement)
          conn.commit()
      except mysql.connector.Error as err:
            print(err.msg)
      else:
          print("OK")
      finally:
         cursor.close()
    else:
      print("Couldn't connect to DB")
    conn.close()

def load_factions():
    conn = connect_to_db()
    if conn and conn.is_connected():
      table_name = 'factions'
      try:
          print("Loading data for table {}: ".format(table_name), end='')
          cursor = conn.cursor()
          for statement in insert_factions:
            cursor.execute(statement)
          conn.commit()
      except mysql.connector.Error as err:
            print(err.msg)
      else:
          print("OK")
      finally:
         cursor.close()
    else:
      print("Couldn't connect to DB")
    conn.close()

from table_data.merchants import insert_merchant as insert_merchant_statement
def load_merchants():
    conn = connect_to_db()
    if conn and conn.is_connected():
      table_name = 'merchant'
      try:
          print("Loading data for table {}: ".format(table_name), end='')
          cursor = conn.cursor()
          cursor.execute(insert_merchant_statement)
          conn.commit()
      except mysql.connector.Error as err:
            print(err.msg)
      else:
          print("OK")
      finally:
         cursor.close()
    else:
      print("Couldn't connect to DB")
    conn.close()

from table_data.npcs import insert_npcs as insert_npc_statement
def load_npcs():
    conn = connect_to_db()
    if conn and conn.is_connected():
      table_name = 'npc'
      try:
          print("Loading data for table {}: ".format(table_name), end='')
          cursor = conn.cursor()
          cursor.execute(insert_npc_statement)
          conn.commit()
      except mysql.connector.Error as err:
            print(err.msg)
      else:
          print("OK")
      finally:
         cursor.close()
    else:
      print("Couldn't connect to DB")
    conn.close()