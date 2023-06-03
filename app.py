from flask import Flask, render_template, jsonify, request, redirect
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

JOBS = [{
  'id': 1,
  'title': 'Data Analyst',
  'location': 'Pune, India',
  'Salary': 'Rs 1,20,000 Per Annum'
}, {
  'id': 2,
  'title': 'Java Dev',
  'location': 'Mumbai, India',
  'Salary': 'Rs 4,00,000 Per Annum'
}, {
  'id': 3,
  'title': 'Python Developer',
  'location': 'Pune, India',
}, {
  'id': 4,
  'title': 'Fluteer Developer',
  'location': 'Remote',
  'Salary': 'Rs 4,22,000 Per Annum'
}]


@app.route("/")
def hello_world():
  return render_template('home.html', jobs=JOBS)


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
  return jsonify(JOBS)


@app.route("/ww")
def contact_usq():
  return render_template("ww.html")


@app.route("/contactus")
def contact_us():
  return render_template("contact.html")


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
