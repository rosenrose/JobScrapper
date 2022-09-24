import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Final


def main():
    BASE_URL: Final = "https://weworkremotely.com"
    term = input("term: ")

    try:
        response = requests.get(f"{BASE_URL}/remote-jobs/search?term={term}")
    except Exception as e:
        print(e)
        return

    if response.status_code != 200:
        print("request failed")
        return

    job_results = []
    soup = BeautifulSoup(response.text, "html.parser")

    sections = soup.select("section.jobs")
    for section in sections:
        jobs = section.select("li:not(.view-all) > a")

        for job in jobs:
            link = urljoin(BASE_URL, job.get("href"))
            company, time, region = job.select("span.company")
            title = job.select_one("span.title")

            job_results.append(
                {
                    "company": company.text,
                    "title": title.text,
                    "time": time.text,
                    "region": region.text,
                    "link": link,
                }
            )

    print(*job_results, sep="\n")


if __name__ == "__main__":
    main()
