from flask import Flask, render_template, request, redirect, url_for, g
import psycopg2

app = Flask(__name__)

def get_db_connection():
  if 'db_connection' not in g:
      g.db_connection = psycopg2.connect(
          host='localhost',
          port='5432',
          dbname='Fullstack',
          user='postgres',
          password='12345'
      )
  return g.db_connection

@app.teardown_appcontext
def close_db_connection(error):
  db_connection = g.pop('db_connection', None)
  if db_connection is not None:
    db_connection.close()

@app.route('/')
def index():
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM data')
  users = cursor.fetchall()
  cursor.close()
  return render_template('index.html', users=users)

@app.route('/user/<int:user_id>')
def view_user(user_id):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM data WHERE id = %s", (user_id,))
  user = cursor.fetchone()
  cursor.close()
  return render_template('view_user.html', user=user)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM data WHERE id = %s", (user_id,))
  user = cursor.fetchone()
  if request.method == 'POST':
      new_username = request.form['user_name']
      new_firstname = request.form['name_first']
      new_lastname = request.form['name_last']
      new_password = request.form['pass_word']
      cursor.execute("UPDATE data SET user_name = %s, name_first = %s, name_last = %s, pass_word = %s WHERE id = %s",
                     (new_username, new_firstname, new_lastname, new_password, user_id))
      conn.commit()
      cursor.close()
      return redirect(url_for('index'))

  cursor.close()
  return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("DELETE FROM data WHERE id = %s", (user_id,))
  conn.commit()
  cursor.close()
  return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
def submit():
  username = request.form['user_name']
  firstname = request.form['name_first']
  lastname = request.form['name_last']
  password = request.form['pass_word']

  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("INSERT INTO data (user_name, name_first, name_last, pass_word) VALUES (%s, %s, %s, %s)",
                 (username, firstname, lastname, password))
  conn.commit()
  cursor.close()

  return redirect('/')

if __name__ == '__main__':
  app.run(debug=True)

# from flask import Flask,render_template,request,redirect,url_for
# import psycopg2

# app = Flask(__name__)

# def get_db_connection():
#   return psycopg2.connect(   
#   host ='localhost',
#   port ='5432',
#   dbname = 'Fullstack',
#   user ='postgres',
#   password ='12345')

# conn = get_db_connection()

# @app.route('/')
# def index():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('select * from data')
#     users = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return render_template('index.html', users = users)
    
# @app.route('/user/<int:user_id>')
# def view_user(user_id):
# # Display details of a single user
#   conn = get_db_connection()
#   cursor = conn.cursor()
#   cursor.execute("SELECT * FROM data WHERE id = %s", (user_id,))
#   user = cursor.fetchone()
#   cursor.close()
#   conn.close()
#   return render_template('view_user.html', user=user)

# @app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
# def edit_user(user_id):
#   # Edit an existing user
#   conn = get_db_connection()
#   cursor = conn.cursor()
#   cursor.execute("SELECT * FROM data WHERE id = %s", (user_id,))
#   user = cursor.fetchone()
#   if request.method == 'POST':
#     new_username = request.form['user_name']
#     new_firstname = request.form['name_first']
#     new_lastname = request.form['name_last']
#     new_password = request.form['pass_word']
#     cursor.execute("UPDATE data SET user_name = %s, name_first = %s, name_last = %s, pass_word = %s WHERE id = %s",(new_username, new_firstname, new_lastname, new_password, user_id))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return redirect(url_for('index'))

#   cursor.close()
#   conn.close()
#   return render_template('edit_user.html', user=user)

# @app.route('/delete_user/<int:user_id>')
# def delete_user(user_id):
#   # Delete an existing user
#   conn = get_db_connection()
#   cursor = conn.cursor()
#   cursor.execute("DELETE FROM data WHERE id = %s", (user_id,))
#   conn.commit()
#   cursor.close()
#   conn.close()
#   return redirect(url_for('index'))

# @app.route('/submit',methods=['POST'])
# def submit():
#   username = request.form['user_name']
#   firstname = request.form['name_first']
#   lastname = request.form['name_last']
#   password = request.form['pass_word']
    

#   cursor = conn.cursor()

#   cursor.execute("INSERT INTO data (user_name,name_first,name_last,pass_word) values (%s,%s,%s,%s)",(username,firstname,lastname,password))

#   conn.commit()

#   cursor.close()
#   conn.close()

#   return redirect('/')
# if __name__ == '__main__':
#   app.run(debug=True)