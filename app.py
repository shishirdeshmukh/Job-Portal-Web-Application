from flask import Flask, render_template, jsonify

app = Flask(__name__)

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
  return render_template("home.html", jobs=JOBS)


@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
