from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import uuid
app=Flask(__name__)

app.config["MYSQL_HOST"]="127.0.0.1"
app.config["MYSQL_USER"]='root'
app.config["MYSQL_PASSWORD"]=''
app.config["MYSQL_DB"]='mydb'

mysql=MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM taskmaster")
    data = cur.fetchall()
    return render_template('index.html',tasks=data)



@app.route('/add',methods=["POST"])
def add_data():
    task = request.form['todo']
    id=uuid.uuid4().hex[:4]
    cur=mysql.connection.cursor()
    cur.execute("INSERT INTO taskmaster(Id,TaskName) VALUES(%s,%s)",(id,task))
    cur.connection.commit()
    cur.close()
    return redirect(url_for('index'))


@app.route('/delete/<id>')
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM taskmaster WHERE Id=%s",([id]))
    cur.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/edit/<id>')
def edit(id):
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM taskmaster WHERE Id=%s",([id]))
    task= cur.fetchone()

    return render_template('edit.html',id=id,task=task)

@app.route('/helper/<id>',methods=["POST"])
def helper(id):
    cur=mysql.connection.cursor()
    task=request.form['task']
    cur.execute("UPDATE taskmaster SET TaskName=%s WHERE Id=%s",([task,id]))
    cur.connection.commit()
    cur.close()
    return redirect(url_for('index'))


if(__name__ == '__main__'):
    app.run(debug=True)