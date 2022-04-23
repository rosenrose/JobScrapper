import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    try:
        pagination = soup.select_one("div.s-pagination")
        links = pagination.select("a")
        # print(links)
        pages = [int(link.text) for link in links[:-1]]
        max_page = pages[-1]
    except:
        return 1

    return max_page


def extract_job(html):
    try:
        title = html.select_one("a[title]")["title"]
        company = html.select_one("h3 span:not([class])").text.strip()
        job_id = html["data-jobid"]
    except Exception as e:
        print(e, html)
        return {}

    try:
        location = html.select_one("h3 span[class]").text.strip()
    except:
        location = ""

    return {
        "site": "Stackoverflow",
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{job_id}/",
    }


def extract_jobs(last_page, url):
    jobs = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }

    for page in range(last_page):
        # for page in range(1):
        print(f"Scraping Stackoverflow page {page + 1}")

        try:
            result = requests.get(f"{url}&pg={page + 1}", headers=headers)
            if result.status_code != 200:
                print("error", result.status_code)
                return []
        except Exception as e:
            print(e, f"{url}&pg={page + 1}")
            return []

        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.select("div.listResults > div.js-result")

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs(query):
    url = f"https://stackoverflow.com/jobs?r=true&q={query}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)

    return jobs
