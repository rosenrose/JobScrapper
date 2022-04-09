import requests
from bs4 import BeautifulSoup

URL = "https://www.indeed.com/jobs?q=python"
LIMIT = 10

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    
    pagination = soup.select_one("div.pagination")
    links = pagination.select("a")
    pages = [int(link.text) for link in links[:-1]]
    max_page = pages[-1]

    return max_page

def extract_job(html):
    title = html.select_one("h2.jobTitle span[title]")["title"]
    company = html.select_one("span.companyName").text.strip()
    locations = html.select_one("div.companyLocation")
    location = remote.text.strip() if (remote := locations.select_one("span:not([class])")) else " ".join([i for i in locations.contents if not hasattr(i, "contents") and len(i.strip())])
    job_id = html["data-jk"]

    return {"title": title, "company": company, "location": location, "link": f"https://www.indeed.com/viewjob?jk={job_id}&vjs=3"}

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
    # for page in range(1):
        print(f"Scraping Indeed page {page + 1}")
        result = requests.get(f"{URL}&start={page * LIMIT}")
        if (result.status_code != 200):
            print("error")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.select("div#mosaic-provider-jobcards > a")
        
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)

    return jobs