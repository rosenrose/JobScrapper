import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  
  pagination = soup.select_one("div.s-pagination")
  links = pagination.select("a")
  pages = [int(link.text) for link in links[:-2]]
  max_page = pages[-1]

  return max_page

def extract_job(html):
  title = html.select_one("a[title]")["title"]
  company = html.select_one("h3 span:not([class])").text.strip()
  location = html.select_one("h3 span[class]").text.strip()
  job_id = html["data-jobid"]

  return {"title": title, "company": company, "location": location, "link": f"https://stackoverflow.com/jobs/{job_id}/"}

def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
  # for page in range(1):
    print(f"Scraping Stackoverflow page {page + 1}")
    result = requests.get(f"{url}&pg={page + 1}")
    if (result.status_code != 200):
      print("error")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.select("div.listResults > div.js-result")
    
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  
  return jobs

def get_jobs(query):
  url = f"https://stackoverflow.com/jobs?q={query}"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)

  return jobs