from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
from typing import Final, List, Dict

BASE_URL: Final = "https://www.indeed.com"

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--headless")


def extract_jobs(query: str, user_agent: str) -> List[Dict[str, str]]:
    options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"{BASE_URL}/jobs?q={query}")
    except Exception as e:
        print(e)
        return

    job_results = []
    soup = BeautifulSoup(driver.page_source, "html.parser")

    jobs = soup.select("ul.jobsearch-ResultsList div.job_seen_beacon")

    for job in jobs:
        # link = urljoin(BASE_URL, job.get("href"))
        # company, time, region = job.select("span.company")
        # title = job.select_one("span.title")

        # job_results.append(
        #     {
        #         "company": company.text,
        #         "title": title.text,
        #         "time": time.text,
        #         "region": region.text,
        #         "link": link,
        #     }
        # )
        ...

    driver.quit()
    return job_results
