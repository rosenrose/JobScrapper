import requests
import urllib.parse
from bs4 import BeautifulSoup

def extract_job(html):
    try:
        title = html.select_one(":scope > a span.title").text.strip()
        company = html.select_one(":scope > a span.company").text.strip()
        link = html.select_one(":scope > a")["href"]
    except Exception as e:
        print(e, html)
        return {}

    try:
        location = html.select_one("a span.region").text.strip()
    except:
        location = ""

    return {
        "site": "Weworkremotely",
        "title": title,
        "company": company,
        "location": location,
        "link": urllib.parse.urljoin("https://weworkremotely.com", link)
    }

def extract_jobs(url):
    jobs = []

    try:
        result = requests.get(url)
        if (result.status_code != 200):
            print("error", result.status_code)
            return []
    except Exception as e:
        print(e, url)
        return []
        
    soup = BeautifulSoup(result.text, "html.parser")
    sections = soup.select("#job_list > section.jobs")
    
    for section in sections:
        section_name = section.select_one("h2 a").text.strip()
        print(f"Scraping Weworkremotely section {section_name}")
        results = section.select("ul li.feature")
        
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    
    return jobs

def get_jobs(query):
    url = f"https://weworkremotely.com/remote-jobs/search?term={query}"
    jobs = extract_jobs(url)

    return jobs
