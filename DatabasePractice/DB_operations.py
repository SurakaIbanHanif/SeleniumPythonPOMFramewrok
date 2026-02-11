#insert, update, delete

insert_query= "insert into student values (6, 'Shovon', 15)"
update_query= "update student set sname= 'Porosh' where sid=6"
delete_query= "delete from student where sid=6"


import mysql.connector

try:
    con=mysql.connector.connect(host=" ", port= " ", user= " ", passwd= " ", database= " ")
    curs=con.cursor()
    curs.execute(delete_query)  #execute query through cursor
    con.commit()    #commit transaction
    con.close()
except:
    print("Connection Unsuccessful")

