from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
from database import engine, load_jobs_from_db, load_job_from_db, add_application_to_db, sign_to_app
from sqlalchemy import text, create_engine
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = os.urandom(24)

ssl_ca = '/etc/ssl/certs/ca-certificates.crt'  # Path to the SSL CA file

conn = mysql.connector.connect(
  host="aws.connect.psdb.cloud",
  user=os.environ['db_user'],
  password=os.environ['db_pass'],
  database="qwerty",
  ssl_ca=ssl_ca,
)

cursor = conn.cursor()


@app.route("/home")
def hello_world():
  if 'id' in session:
    try:
      jobs = load_jobs_from_db()
      return render_template('home.html', jobs=jobs)
    except Exception as e:
      return render_template('error.html', error=str(e))
  else:
    return redirect('login.html')


@app.route("/signup")
def signup():
  return render_template('signup.html')


@app.route("/")
def login():
  return render_template('login.html')


@app.route("/login_vald", methods=['POST'])
def login_vald():
  try:
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute(
      """SELECT * from `users` WHERE `email` LIKE '{}' AND `password`  LIKE '{}'"""
      .format(email, password))
    users = cursor.fetchall()
    if len(users) > 0:
      session['id'] = users[0][0]
      return redirect('/home')
    else:
      flash("Wrong Details")
      return redirect('/')
  except Exception as e:
    return render_template('error.html', error=str(e))


@app.route("/add_user", methods=['POST'])
def add_user():
  try:
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    hashed_password = generate_password_hash(password)

    query = """INSERT INTO `users` (`id`, `name`, `email`, `password`) VALUES (NULL, %s, %s, %s)"""
    values = (name, email, hashed_password)

    cursor.execute(query, values)
    conn.commit()

    cursor.execute("""SELECT * FROM `users` WHERE `email` = %s""", (email, ))
    myuser = cursor.fetchall()
    session['id'] = myuser[0][0]

    flash("User Registered Successfully")

    return redirect('/')
  except Exception as e:
    return render_template('error.html', error=str(e))


@app.route("/job/<id>")
def showjob(id):
  job = load_job_from_db(id)
  if job:
    return render_template('jobpage.html', job=job)
  else:
    return render_template('jobnotfound.html')


@app.route("/api/job/<id>")
def show_job_json(id):
  job = load_job_from_db(id)
  return jsonify(job)


@app.route("/logout")
def logout():
  session.pop('id')
  return redirect('/')


@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  data = request.form
  job = load_job_from_db(id)
  add_application_to_db(id, data)
  return render_template('application_submitted.html',
                         application=data,
                         job=job)


@app.route("/upload")
def up():
  return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
  try:
    file = request.files['file']
    if file:
      file.save(
        os.path.join(app.config['UPLOAD_DIRECTORY'],
                     secure_filename(file.filename)))
    else:
      return redirect('/upload')

  except RequestEntityTooLarge:
    return 'File is Larger than 16 MB Limit'
    return redirect('/upload')
  return redirect('/')


@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)


@app.route("/contactus")
def contact_us():
  return render_template("contact.html")


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
