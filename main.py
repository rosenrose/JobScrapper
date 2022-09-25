import os
import json
from pathlib import Path
from flask import Flask, render_template, request, redirect, send_file
from extractors import wwr, indeed
from export import save_to_csv
from typing import Final

USER_AGENT: Final = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"

cache: dict[str, list] = {}
if (saved_cache := Path("cache.json")).exists():
    cache = json.load(open(saved_cache, encoding="utf-8"))

app = Flask("JobScrapper")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("query")

    if (not query) or (not query.strip()):
        return redirect("/")

    query_key = query.lower()

    if query_key in cache:
        jobs = cache[query_key]
    else:
        wwr_results = wwr.extract_jobs(query_key, USER_AGENT)
        indeed_results = indeed.extract_jobs(query_key, USER_AGENT)

        jobs = wwr_results + indeed_results
        cache[query_key] = jobs
        json.dump(cache, open(saved_cache, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    return render_template("search.html", query=query, jobs=jobs)


@app.route("/export")
def export():
    query = request.args.get("query")
    format = request.args.get("format")

    if (not query) or (not query.strip()):
        return redirect("/")

    query_key = query.lower()

    if (query_key not in cache) or (not format) or (not format.strip()):
        return redirect(f"/search?query={query}")

    filename = f"{query}.{format.lower()}"
    jobs = cache[query_key]

    match format.lower():
        case "csv":
            save_to_csv(filename, jobs)
        case "json":
            json.dump(
                jobs,
                open(filename, "w", encoding="utf-8"),
                ensure_ascii=False,
                indent=2,
            )
        case _:
            return redirect(f"/search?query={query}")

    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run("0.0.0.0", port=os.environ.get("PORT", 5000))
