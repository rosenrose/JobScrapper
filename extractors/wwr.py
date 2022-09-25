import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Final, List, Dict

BASE_URL: Final = "https://weworkremotely.com"


def extract_jobs(query: str, user_agent: str) -> List[Dict[str, str]]:
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
            company, time, location = job.select("span.company")
            title = job.select_one("span.title")

            job_results.append(
                {
                    "company": company.text.strip(),
                    "title": title.text.strip(),
                    "time": time.text.strip(),
                    "location": location.text.strip(),
                    "link": link,
                }
            )

    return job_results
