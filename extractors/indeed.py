import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
from typing import Final

BASE_URL: Final = "https://www.indeed.com"
MAX_PAGE: Final = 5

driver: webdriver.Chrome = None

location_regex = re.compile(r"[+]\d+\s*location[s]?")
metadata_regex = re.compile(r"[+]\d+")


def get_page_count(query: str) -> int:
    try:
        driver.get(f"{BASE_URL}/jobs?q={query}")
    except Exception as e:
        print(e)
        return 0

    soup = BeautifulSoup(driver.page_source, "html.parser")
    pagination = soup.select_one("ul.pagination-list")

    if pagination == None:
        return 1

    page_count = len(pagination.select("li"))

    return min(page_count, MAX_PAGE)


def extract_indeed_jobs(query: str, page: int) -> list[dict[str, str]]:
    try:
        driver.get(f"{BASE_URL}/jobs?q={query}&start={page * 10}")
    except Exception as e:
        print(e)
        return []

    job_results = []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = soup.select("ul.jobsearch-ResultsList div.job_seen_beacon")

    for job in jobs:
        title = job.select_one("h2.jobTitle a")
        link = urljoin(BASE_URL, title.get("href"))
        company = job.select_one("span.companyName")

        locationWrapper = job.select_one("div.companyLocation")
        # print(list(locationWrapper.children), [type(i) for i in locationWrapper.children])
        location = location_regex.sub("", locationWrapper.text).strip()
        # print(locationWrapper.text, "->", location)

        metadata = job.select("div.metadata:not([class*='salary'])")
        time = " / ".join([metadata_regex.sub("", i.text).strip() for i in metadata])

        job_results.append(
            {
                "company": company.text.strip(),
                "title": title.text.strip(),
                "time": time,
                "location": location,
                "link": link,
            }
        )

    return job_results


def extract_jobs(query: str, user_agent: str) -> list[dict[str, str]]:
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")
    options.add_argument(f"user-agent={user_agent}")
    global driver
    driver = webdriver.Chrome(service=service, options=options)

    page_count = get_page_count(query)
    # print(page_count)

    results = []
    for page in range(page_count):
        results += extract_indeed_jobs(query, page)
        time.sleep(1.2)

    driver.quit()

    return results
