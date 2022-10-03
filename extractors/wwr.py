import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Final

BASE_URL: Final = "https://weworkremotely.com"


def extract_jobs(query: str, user_agent: str) -> list[dict[str, str]]:
    try:
        response = requests.get(
            f"{BASE_URL}/remote-jobs/search?term={query}", headers={"User-Agent": user_agent}
        )
    except Exception as e:
        print(e)
        return []

    if response.status_code != 200:
        print("request failed")
        return []

    job_results = []

    soup = BeautifulSoup(response.text, "html.parser")
    sections = soup.select("section.jobs")

    for section in sections:
        jobs = section.select("li:not(.view-all) > a")

        for job in jobs:
            link = urljoin(BASE_URL, job.get("href"))

            try:
                company, time, location = job.select("span.company")
            except:
                company, time = job.select("span.company")
                location = None

            title = job.select_one("span.title")

            job_results.append(
                {
                    "company": company.text.strip(),
                    "title": title.text.strip(),
                    "time": time.text.strip(),
                    "location": location.text.strip() if location else "",
                    "link": link,
                }
            )

    return job_results
