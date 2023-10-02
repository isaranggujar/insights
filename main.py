import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Admins@2023",
  database="mydb"
)

mycursor = mydb.cursor()

'mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")'
mycursor.execute("DROP TABLE customers")
mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = ("John", "Highway 21")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
