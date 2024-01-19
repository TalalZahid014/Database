from flask import Flask,render_template,request,redirect
import psycopg2

app = Flask(__name__)

DB_HOST ='localhost'
DB_PORT ='5432'
DB_NAME = 'Fullstack'
DB_USER ='postgres'
DB_PASSWORD ='12345'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit',methods=['POST'])
def submit():
    username = request.form['user_name']
    firstname = request.form['name_first']
    lastname = request.form['name_last']
    password = request.form['pass_word']

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cursor = conn.cursor()

    cursor.execute("INSERT INTO data (user_name,name_first,name_last,pass_word) values (%s,%s,%s,%s)",(username,firstname,lastname,password))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=300)