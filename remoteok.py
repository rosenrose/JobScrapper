import requests
import urllib.parse
from bs4 import BeautifulSoup


def extract_job(html):
    try:
        title = html.select_one("td.company h2[itemprop='title']").text.strip()
        company = html.select_one("td.company h3[itemprop='name']").text.strip()
        link = html["data-url"]
    except Exception as e:
        print(e, html)
        return {}

    try:
        location = html.select_one("div.location").text.strip()
    except:
        location = ""

    return {
        "site": "Remoteok",
        "title": title,
        "company": company,
        "location": location,
        "link": urllib.parse.urljoin("https://remoteok.com", link),
    }


def extract_jobs(url):
    jobs = []
    print(f"Scraping Remoteok")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }

    try:
        result = requests.get(url, headers=headers)
        if result.status_code != 200:
            print("error", result.status_code)
            return []
    except Exception as e:
        print(e, url)
        return []

    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.select("table#jobsboard tr.job")

    for result in results:
        job = extract_job(result)
        jobs.append(job)

    return jobs


def get_jobs(query):
    url = f"https://remoteok.io/remote-dev+{query}-jobs"
    jobs = extract_jobs(url)

    return jobs
