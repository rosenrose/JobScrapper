import os
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, redirect, send_file
from extractors import wwr, indeed
from export import save_to_csv, save_to_json
from typing import Final

USER_AGENT: Final = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"

CACHE_REFRESH_RATE_SECONDS = 60 * 60
cache: dict[str, dict] = {}
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
    is_refresh_force = request.args.get("refresh_force") != None

    if is_ignore_cache(is_refresh_force, query_key):
        wwr_results = wwr.extract_jobs(query_key, USER_AGENT)
        indeed_results = indeed.extract_jobs(query_key, USER_AGENT)

        jobs = wwr_results + indeed_results

        cache[query_key] = {"timestamp": str(datetime.now()), "data": jobs}
        json.dump(cache, open(saved_cache, "w", encoding="utf-8"))
    else:
        jobs = cache[query_key]["data"]

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

    jobs = cache[query_key]["data"]

    match format.lower():
        case "csv":
            output = save_to_csv(jobs)
        case "json":
            output = save_to_json(jobs)
        case _:
            return redirect(f"/search?query={query}")

    filename = f"{query}.{format.lower()}"

    return send_file(output, download_name=filename, as_attachment=True)


def is_ignore_cache(is_refresh_force: bool, query_key: str) -> bool:
    if is_refresh_force:
        return True

    if query_key not in cache:
        return True

    timestamp = datetime.fromisoformat(cache[query_key]["timestamp"])

    return (datetime.now() - timestamp).seconds > CACHE_REFRESH_RATE_SECONDS


if __name__ == "__main__":
    app.run("0.0.0.0", port=os.environ.get("PORT", 5000))
