import sqlite3


def add_food(recepie,instruction,email,img):
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO Food (Recepies,Instruction,email,image) VALUES (?,?,?,?)",(recepie,instruction,email,img))
    conn.commit()
    conn.close()    
    
def add_user(username,password,email):
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO users (username,password,email) VALUES (?,?,?)",(username,password,email))
    conn.commit()
    conn.close()

def search_email(email):
    conn = sqlite3.connect('database.db')
    #email = 'a@g.com'
    result = conn.execute("SELECT email from users WHERE email ='{}'".format(email))
    result = result.fetchall()
    conn.commit()
    conn.close()
    return  result       

def search_password(email):
    conn = sqlite3.connect('database.db')
    #email = 'a@g.com'
    result = conn.execute("SELECT password from users WHERE email ='{}'".format(email))
    result = result.fetchall()
    result = result[0][0]
    conn.commit()
    conn.close()
    return  result  

def get_food_image(recepie):
    conn = sqlite3.connect('database.db')
    #recepie = 'a'
    result = conn.execute("SELECT  image from Food WHERE Recepies ='{}'".format(recepie))
    result = result.fetchall()
    result = (result[0][0])
    conn.commit()
    conn.close()
    return  result    

def get_recepies_email(email):
    conn = sqlite3.connect('database.db')
    result = conn.execute("SELECT  Recepies,image from Food WHERE email ='{}'".format(email))
    result = result.fetchall()
    #result = (result[0])
    conn.commit()
    conn.close()
    return  result
def get_recepies():
    conn = sqlite3.connect('database.db')
    result = conn.execute("SELECT  Recepies,image from Food")
    result = result.fetchall()
    #result = (result[0])
    conn.commit()
    conn.close()
    return  result

def get_recepies_info(recepie):
    conn = sqlite3.connect('database.db')
    #recepie = 'a'
    result = conn.execute("SELECT  instruction from Food WHERE Recepies ='{}'".format(recepie))
    result = result.fetchall()
    result = result[0][0]
    conn.commit()
    conn.close()
    return  result

def update(recepies,instruction,image,email,old_title):
     conn = sqlite3.connect('database.db')

     if image!="":
         text = "UPDATE Food SET Recepies ='{}',Instruction ='{}',image='{}' WHERE Recepies='{}' AND email ='{}' ".format(recepies,instruction,image,old_title,email)
         update = conn.execute(text)
     else:
         text = "UPDATE Food SET Recepies='{}',Instruction='{}' WHERE Recepies='{}' AND email ='{}' ".format(recepies,instruction,old_title,email)
         update = conn.execute(text)

     
     update = update.fetchall()
     conn.commit()
     conn.close()
    
def delete(recepie,email):    
    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM Food WHERE Recepies='{}' AND email ='{}'".format(recepie,email))
    conn.commit()
    conn.close()
    
