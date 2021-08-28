# -*- coding: utf-8 -*-

# DB Settings
DB_HOST = "localhost"   
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "123"
DB_PORT = "5432"



import psycopg2
import pandas as pd
from datetime import datetime

df = pd.read_excel("users.xlsx",)
# df = pd.read_csv("users.csv")

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host = DB_HOST, port = DB_PORT)

cur = conn.cursor()

for count,value in enumerate(df['username']):
    
    # For user_info table in db
    user_info_username = df['username'][count]
    user_info_password = df['password'][count]
    user_info_is_staff = str(df['is_staff'][count])
    user_info_first_name_last_name = df['name'][count]
    user_info_email = df['email'][count]
    user_info_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # For match_user_group table in db
    user_group_id = str(df['group_id'][count])
    
    # Query for user_info table 
    query1 = """INSERT INTO user_info (username, password, is_staff, first_name_last_name, email, date) VALUES (%s, %s, %s, %s, %s, %s)"""
    values1 = (user_info_username,user_info_password,user_info_is_staff,user_info_first_name_last_name,user_info_email,user_info_date)
    
    cur.execute(query1, values1)
    conn.commit()
    
    # Get id from user_info table
    query2 = """ SELECT * FROM user_info WHERE username= %s """
    value2 = (user_info_username ,)
    cur.execute(query2, value2)
    
    
    user_id_from_user_info = str(cur.fetchall()[0][6])
    print(user_id_from_user_info)
    print(user_group_id)
    
    # Query for match_user_group table
    query3 = """INSERT INTO match_user_group (user_id, group_id) VALUES (%s, %s)"""
    values3 = (user_id_from_user_info, user_group_id)
    cur.execute(query3,values3)
    conn.commit()

    
conn.close()
