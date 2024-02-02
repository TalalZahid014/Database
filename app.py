from flask import Flask,render_template,request,redirect
import psycopg2

app = Flask(__name__)

def get_db_connection():
  return psycopg2.connect(   
  host ='localhost',
  port ='5432',
  dbname = 'Fullstack',
  user ='postgres',
  password ='12345')

conn = get_db_connection()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('select * from data')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', users = users)
    
@app.route('/user/<int:user_id>')
def view_user(user_id):
# Display details of a single user
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM data WHERE id = %s", (user_id,))
  user = cursor.fetchone()
  cursor.close()
  conn.close()
  return render_template('view_user.html', user=user)

@app.route('/submit',methods=['POST'])
def submit():
  username = request.form['user_name']
  firstname = request.form['name_first']
  lastname = request.form['name_last']
  password = request.form['pass_word']
    

  cursor = conn.cursor()

  cursor.execute("INSERT INTO data (user_name,name_first,name_last,pass_word) values (%s,%s,%s,%s)",(username,firstname,lastname,password))

  conn.commit()

  cursor.close()
  conn.close()

  return redirect('/')
if __name__ == '__main__':
  app.run(debug=True)