from flask import Flask, render_template, jsonify, request, redirect
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
from database import engine, load_jobs_from_db
from sqlalchemy import text

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/")
def hello_world():
  jobs = load_jobs_from_db()
  return render_template('home.html', jobs=jobs)


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


@app.route("/ww")
def contact_usq():
  return render_template("ww.html")


@app.route("/contactus")
def contact_us():
  return render_template("contact.html")


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
