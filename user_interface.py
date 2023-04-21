''' ------------------------------------------------------------------------      user interface ---------------------------
SIGN IN SIGN UP
CART_TABLE FUNCTION OPERATIONS - CREATE CART _TABLE

'''

import mysql.connector as sql
import pandas as pd
import info


info_array = [info.host,info.user,info.password]

mydb = sql.connect(host = info_array[0],user = info_array[1],password = info_array[2], database = "project_db")
cursor = mydb.cursor(buffered=True)
cursor.execute("""CREATE TABLE IF NOT EXISTS cart_table
               (itemid int(3) primary key,
               itemname varchar(20),
               price float(10,2),
               quantity int(3),
               totalprice float(100,2))""")
cursor.execute("""CREATE TABLE IF NOT EXISTS user_table 
               (user_id int NOT NULL PRIMARY KEY, 
                name varchar(30),
                password varchar(30), 
                email_id varchar(30), 
                address VARCHAR(255))""")

cursor.execute("SELECT * FROM user_table ORDER BY user_id DESC")
userid=cursor.fetchall()
last_id = userid[0][0]
new_id = last_id + 1

## note keep the itemid and prod_id from cart and product table same 

## ---------------------------------- sign in / sign up -----------------------------
def SignIn(): 
    signin = False# some flow control thats removable
    while not signin:
        signin_email = str(input("----Email: ".upper()))# input for email
        signin_password = str(input("----Password: ".upper()))# input for password

        cursor.execute("SELECT user_id,email_id,password,name FROM user_table WHERE email_id = %s and password=%s",(signin_email,signin_password))
        results = cursor.fetchall()
        row_count = cursor.rowcount
        # this if else is used to know if there is an existing id or is this the users first sign in 
        if row_count==0:
            print("***unrecognized email or password***".upper())
            return '0'
        else:
            signin=True
            print(f'Welcome {results[0][3].capitalize()}'.upper())
            return [signin_email,signin_password]
        
def SignUp(userid):
    signup_name = str(input("----Set Name: ".upper()))#main name

    correct_signup=False
    while not correct_signup:
        #----------------to check email is valid or not
        email_unique = False
        while not email_unique:
            signup_user_email = str(input("----Set Email ID: ".upper()))#main email
            find_com=signup_user_email.find(".com") 
            find_A=signup_user_email.find('@')

            if find_com==-1 or find_A==-1:
                print("***Invalid Email ID, Please Make Sure Your Email Has '@' and '.com'***".upper())
            elif (signup_user_email=="ADMIN@ADMIN.COM" or signup_user_email=="admin@admin.com") :
                print("***Invalid Email ID, This Email Cannot Be Used ***".upper())
                
            else:
                correct_signup=True

                
            #----------------checks whether email is unique or not
                cursor.execute(f"SELECT email_id FROM user_table WHERE email_id= '{signup_user_email}'")
                results = cursor.fetchall()
                row_count = cursor.rowcount

                if row_count==0: #means the email is unique
                    
                    email_unique = True
                    #-------------checks if passwd and confirm passwd are equal
                    p1_equal_p2= False
                    while not p1_equal_p2:
                        Invalidpass=True
                        while Invalidpass:
                            passwd1 = str(input("----Set Password: ".upper()))
                            if len(passwd1)>30:
                                print("***Invalid Password, Password Length Should Be Less Than 30 Characters***".upper())
                            else:
                                Invalidpass=False
                        passwd2 = str(input("----Confirm Password: ".upper()))
                        if passwd1 == passwd2:
                            signup_passwd = passwd1#main passwd
                            signup_user_address = str(input("----Set Address: ".upper()))#main address
                            break
                        else:
                            print('***Passwords DO NOT Match***'.upper())
                            p1_equal_p2 = False
                            
                    #--------------inserts the signup values into mysql
                    sql = f"INSERT INTO user_table (user_id,name,password,email_id,address) VALUES (%s,%s,%s,%s,%s)"
                    val =(userid, signup_name,signup_passwd,signup_user_email,signup_user_address)
                    cursor.execute(sql, val)
                    mydb.commit()
                    print('****=Your Account Has Been Created Successfully=****'.upper())
                    input("PRESS ENTER TO CONTINUE")
                    
                else: #means email is not unique
                    print("***This Email ID Already Exists, Please Try Again***".upper())
                    print("***PLEASE SIGN-IN OR USE ANOTHER EMAIL***")
                    input("PRESS ENTER TO CONTINUE")
                    email_unique = True

#-------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------CART FUNCTIONSSSSS----------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------


def view_cart():
    cursor.execute("select * from cart_table")        
    results = cursor.fetchall()
    results1 = pd.DataFrame(results)
    print(results1)



def delete_cartitem(itemid,itemq):
    
    cursor.execute(f"SELECT quantity FROM cart_table WHERE itemid={itemid}")
    orginal_quantity=cursor.fetchone()[0]
    
    if itemq== orginal_quantity:
        cursor.execute(f"delete from cart_table where itemid={itemid}")
        mydb.commit()

    else:
        newquantity=orginal_quantity-itemq
        cursor.execute(f"SELECT price FROM cart_table WHERE itemid={itemid}")
        price=cursor.fetchone()[0]
        totalprice=price*newquantity
        f"update cart_table set quantity={newquantity},totalprice={totalprice} where itemid={itemid}"
        
        cursor.execute(f"update cart_table set quantity={newquantity},totalprice={totalprice} where itemid={itemid}")
        mydb.commit()



def add_product_to_cart(itemid,itemquantity):
    
    cursor.execute(f"select price from product_table where prod_ID ={itemid}")
    item_price = cursor.fetchone()[0]
    
    totalprice = item_price*itemquantity
    cursor.execute(f"select prod_name from product_table where prod_ID = {itemid}")
    item_name = cursor.fetchone()[0]
    
    val=(itemid,item_name,item_price,itemquantity,totalprice)   
    cursor.execute("insert into cart_table values(%s,%s,%s,%s,%s)",val)

    mydb.commit()
    # here changing the original quantity
    cursor.execute(f"select prod_quantity from product_table where prod_ID = {itemid}")
    initial_item_quantity  = cursor.fetchone()[0]
    final_item_quantity = initial_item_quantity-itemquantity
    cursor.execute(f"update product_table set prod_quantity = {final_item_quantity} where prod_ID = {itemid}")

    
            



            
    
def increment_quantity(itemid):
    cursor.execute(f"select quantity from cart_table where itemid = {itemid}")
    q = cursor.fetchone()[0]
    q = q+1
    cursor.execute(f"update cart_table set quantity = {q} where itemid = {itemid}")


def decrement_quantity(itemid):
    cursor.execute(f"select quantity from cart_table where itemid = {itemid}")
    q = cursor.fetchone()[0]
    q = q-1
    cursor.execute(f"update cart_table set quantity = {q} where itemid = {itemid}")

# all the functions for user interface 
# this will have three interfaces 
#"""
# 1. sign up sign in 
# from the sign up sign in if the user signs in as admin@admin.com and pass = admin123 we go to the admin interface 
# if not then user signin checks if the sign in is correct and give three tries for correct sign in then moves to exit status
#
# 2. main menu 
#   - shop(the finctions in shop would be add_items_to_cart - user would see the product_table and put things from that intp cart_table )
#
#   - checkout
#this will have few functions namely delete item
# the + and - button
#
# "