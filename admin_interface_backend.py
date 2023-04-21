''' --------------------------------------------------------------- THIS IS THE ADMIN INTERFACE-----------------------------------------------------'''

import mysql.connector as sql
import pandas as pd
import info


info_array = [info.host,info.user,info.password]

mydb = sql.connect(host = info_array[0],user = info_array[1],password = info_array[2])
cursor = mydb.cursor()

## database name to be changed
cursor.execute("Create database IF NOT EXISTS project_db")
cursor.execute("use project_db")

cursor.execute("""Create table if not exists product_table
                (prod_ID varchar(50) primary key
               ,prod_name varchar(50)
               ,prod_quantity int(5) 
               ,price float (10,2))""")

cursor.execute("""CREATE TABLE IF NOT EXISTS user_table 
               (user_id int NOT NULL PRIMARY KEY, 
                name varchar(30),
                password varchar(30), 
                email_id varchar(30), 
                address VARCHAR(255))""")

##------- making the admin login-----
cursor.execute("SELECT email_ID, password FROM user_table WHERE email_ID = 'ADMIN@ADMIN.COM' and password = 'ADMIN123'")
cursor.fetchall()

if cursor.rowcount == 0:
    cursor.execute("INSERT INTO user_table VALUES (000, 'ADMIN', 'ADMIN123', 'ADMIN@ADMIN.COM', 'REDACTED')")
    mydb.commit()
else:
    pass


##-----------------------------------------------------INPUT FOR TABLE------------------------------------
# prod_id = input("enter product id ")
# prod_name = input("enter the product name")
# prod_quant = int(input('enter the quantity of product in inventory'))
# price = float(input("enter teh price of the item"))




def insert_item(prod_id,prod_name,prod_quant,price):
    sql="insert into product_table values(%s,%s,%s,%s)"
    val=(prod_id,prod_name,prod_quant,price)
    cursor.execute(sql,val)
    mydb.commit()
    
    
    
def show_table_product():
    cursor.execute(f"select * from product_table order by prod_ID ASC")
    table_output = cursor.fetchall()
    #----------------------------------------------------------------------------------output---------------------------------------
    df = pd.DataFrame(table_output)
    print(df)



def clear_table():
    cursor.execute("truncate product_table")
    

def delete_item(prod_id):
    cursor.execute(f"DELETE FROM product_table WHERE prod_Id={prod_id}")
    mydb.commit()

    print(f"ITEM WITH ITEM ID {prod_id} HAS BEEN DELTED")
    show_table_product()

def show_table_user():
    cursor.execute(f"select * from user_table order by user_id ASC")
    table_output = cursor.fetchall()
    #----------------------------------------------------------------------------------output---------------------------------------
    df = pd.DataFrame(table_output)
    print(df)

def changeprice_item(price,prod_id):
    cursor.execute(f"UPDATE product_table SET price={price} where prod_ID={prod_id}")
    mydb.commit()

    print("PRICE CHANGED SUCCESFULLY")
    show_table_product()


def changename_item(prod_name,prod_id):
    cursor.execute(f"UPDATE product_table SET prod_name='{prod_name}' where prod_ID={prod_id}")
    mydb.commit()

    print("ITEM NAME CHANGED SUCCESFULLY")
    show_table_product()


##------------------ readme----------------------"""
# the admin page has the following functions
# 1)ENTER NEW ITEM

# 2)DELETE OLD ITEM
# 3)CHANGE PRICE
# 4) change item name
# the program makes the user_table product_table and also inputs the first entry in user_table as the admin



    








