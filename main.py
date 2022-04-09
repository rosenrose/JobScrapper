from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")
cache = {}
CSV_NAME = "jobs.csv"

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  if query := request.args.get("query"):
    query = query.lower()
    if query in cache:
      jobs = cache[query]
    else:
      jobs = get_jobs(query)
      cache[query] = jobs
  else:
    return redirect("/")

  return render_template("report.html", resultsNumber=len(jobs), searchBy=query, jobs=jobs)

@app.route("/export")
def export():
  try:
    if query := request.args.get("query"):
      query = query.lower()
    else:
      raise Exception()

    jobs = cache[query]
    save_to_file(CSV_NAME, jobs)
    return send_file(CSV_NAME)
  except:
    return redirect("/")

app.run(host="0.0.0.0")