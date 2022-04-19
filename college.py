import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  port='',
  database="college"
)
command_handler = db.cursor(buffered=True)

def teacher_session():
  while 1:
    print("")
    print("Teacher login")
    print("1. Mark Student register ")
    print("2. view register")
    print("3. Logout")

    user_option = input(str("Options: "))
    if user_option =="1":
      print("")
      print("Mark student register")
      command_handler.execute("SELECT username FROM users WHERE privilege = 'Student'")
      records = command_handler.fetchall()
      date = input(str("Date : DD/MM/YYYY"))
      for record in records:
        record = str(record).replace("'", "")
        record = str(record).replace(",", "")
        record = str(record).replace("(", "")
        record = str(record).replace(")", "")
        status = input(str("Status for "+ str(record )+ "P/A/L : "))
        query_vals = (str(record), date, status)
        command_handler.execute("INSERT INTO attendance (username, date, status) VALUES (%s,%s,%s)", query_vals)
        db.commit()
        print(record + "Marked as " + status)
    elif user_option =="2":
      print("")
      print("Viewing all student registers")
      command_handler.execute("SELECT username, date, status FROM attendance")
      records = command_handler.fetchall()
      for record in records:
        print(record)
    elif user_option =="3":
      break
    else:
      print("No valid option selected")

def student_session(username):
  while 1:
    print("")
    print("Student Menue")
    print("")
    print("1. View Register")
    print("2. Download Register")
    print("3. Logout")
    user_option = input(str("Options: "))
    if user_option == "1":
      print("Displaying register")
      username = (str(username),)
      command_handler.execute("SELECT username, date, status FROM attendance WHERE  username = %s",username)
      records = command_handler.fetchall()
      for record in records:
        print(record)
    elif user_option =="2":
      print("Downloading Register")
      username = (str(username),)
      command_handler.execute("SELECT username, date, status FROM attendance WHERE username = %s", username)
      records = command_handler.fetchall()
      for record in records:
        with open("/Users/thesoftwareengineer./Desktop/register.txt", "w") as f:
          f.write(str(records)+ "\n")
        f.close()
      print("All record saved")

    elif user_option == "3":
      break
    else:
      print("No valied option selected")


def admin_session():
  while 1:
    print("")
    print("Admin login")
    print("1. Register new Student ")
    print("2. Register new Teacher")
    print("3. Delete Existing Student")
    print("4. Delete Existing Teacher")
    print("5. Logout")

    user_option = input(str("Option:  "))
    if user_option =="1":
      print("")
      print("Register new Student")
      username = input(str("Student username"))
      password = input(str("Student password"))
      query_vals = (username,password)
      command_handler.execute("INSERT INTO users (username,password,privilege) VALUES (%s,%s, 'Student')", query_vals)
      db.commit()
      print(username+ " has been registered as student")
    elif user_option =="2":
      print("")
      print("Register new Teacher")
      username = input(str("Teacher username: "))
      password = input(str("Teacher password: "))
      query_vals = (username, password)
      command_handler.execute("INSERT INTO users (username,password,privilege) VALUES (%s,%s, 'Teacher')", query_vals)
      db.commit()
      print(username + " has been registered as Teacher")
    elif user_option =="3":
      print("")
      print("Delete Existing Student Account")
      username = input(str("Student username: "))
      query_vals = (username, "Student")
      command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
      db.commit()
      if command_handler.rowcount < 1:
        print("User not found")
      else:
        print(username+" has been deleted !")
    elif user_option =="4":
      print("")
      print("Delete Existing Teacher Account")
      username = input(str("Teacher username: "))
      query_vals = (username, "Teacher")
      command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
      db.commit()
      if command_handler.rowcount < 1:
        print("User not found")
      else:
        print(username + " has been deleted !")
    elif user_option =="5":
      break
    else:
      print("No valid option was selected ")


def auth_student():
  print("")
  print("Student login")
  print("")
  username = input(str("Username: "))
  password = input(str("Password: "))
  query_vals = (username, password, "student")
  command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s and privilege = %s", query_vals)
  if command_handler.rowcount <= 0:
    print("Invalid login details")
  else:
    student_session(username)

def auth_teacher():
  print("")
  print("Teacher login")
  print("")
  username = input(str("Username: "))
  password = input(str("Password: "))
  query_vals = (username,password)
  command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'Teacher' ", query_vals)
  if command_handler.rowcount <= 0:
    print("Login not recognized")
  else:
    teacher_session()


def auth_admin():
  print("")
  print("Admin login")
  print("")
  username= input(str("username: "))
  password= input(str("password: "))

  if username == "admin":
    if password == "password":
      admin_session()
    else:
      print("inccorect password !")
  else:
    print("Login detail not recognized")



def main():
  while 1:
    print("Welcome to the college system")
    print("")
    print("1. Login as student")
    print("2. Login as teacher")
    print("3. Login as admin")

    user_option = input(str("Option: "))
    if user_option== "1":
      auth_student()
    elif user_option== "2":
      auth_teacher()
    elif user_option =="3":
      auth_admin()
    else:
      print("No valid option was selected")
main()

