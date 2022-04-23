"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

from flask import Flask, render_template, request, redirect, send_file

# from stackoverflow import get_jobs as get_stackoverflow_jobs
from weworkremotely import get_jobs as get_weworkremotely_jobs
from remoteok import get_jobs as get_remoteok_jobs
from indeed import get_jobs as get_indeed_jobs
from exporter import save_to_file
from functools import reduce
import random

app = Flask("SuperScrapper")
cache = {}
CSV_NAME = "jobs.csv"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    if query := request.args.get("query"):
        query = query.lower().strip()
        if query in cache:
            jobs = cache[query]
        else:
            # jobs = get_remoteok_jobs(query)
            jobs = {
                # "Stackoverflow": [i for i in get_stackoverflow_jobs(query) if len(i.keys())],
                "Indeed": [i for i in get_indeed_jobs(query) if len(i.keys())],
                "Weworkremotely": [
                    i for i in get_weworkremotely_jobs(query) if len(i.keys())
                ],
                "Remoteok": [i for i in get_remoteok_jobs(query) if len(i.keys())],
            }
            cache[query] = jobs
        resultsNumber = reduce(lambda x, y: x + len(y), jobs.values(), 0)
    else:
        return redirect("/")

    return render_template(
        "report.html", resultsNumber=resultsNumber, searchBy=query, jobs=jobs
    )


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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
