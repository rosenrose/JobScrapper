import requests
from bs4 import BeautifulSoup

LIMIT = 10


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.select_one("div.pagination")
    links = pagination.select("a")
    pages = [int(link.text) for link in links[:-1]]
    max_page = pages[-1]

    return max_page


def extract_job(html):
    try:
        title = html.select_one("h2.jobTitle span[title]")["title"]
        company = html.select_one("span.companyName").text.strip()
        job_id = html["data-jk"]
    except Exception as e:
        print(e, html)
        return {}

    try:
        locations = html.select_one("div.companyLocation")
        location = (
            remote.text.strip()
            if (remote := locations.select_one("span:not([class])"))
            else " ".join(
                [
                    i
                    for i in locations.contents
                    if not hasattr(i, "contents") and len(i.strip())
                ]
            )
        )
    except:
        location = ""

    return {
        "site": "Indded",
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://www.indeed.com/viewjob?jk={job_id}&vjs=3",
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        # for page in range(1):
        print(f"Scraping Indeed page {page + 1}")

        try:
            result = requests.get(f"{url}&start={page * LIMIT}")
            if result.status_code != 200:
                print("error")
        except Exception as e:
            print(e, f"{url}&pg={page + 1}")
            return []

        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.select("div#mosaic-provider-jobcards > a")

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs(query):
    url = f"https://www.indeed.com/jobs?q={query}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)

    return jobs
