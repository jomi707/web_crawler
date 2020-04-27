import requests
from bs4 import BeautifulSoup

URL = "https://kr.indeed.com/jobs?q=python&limit=50"

def extract_indeed_pages():
    result = requests.get(URL)

    # BeautifulSoup object.text
    soup = BeautifulSoup(result.text, "html.parser")

    # div class is pagination
    pagination = soup.find("div", {"class":"pagination"})
    # span class is pn
    links = pagination.find_all('span', {"class":"pn"})
    pages = []

    for link in links:
        pages.append(link.string)

    last_page = pages[-2]
    return int(last_page)
    # append page number

    # html.a["attribute"] == take a attribute's value

def extract_job(html):
    title = html.find('a')['title']
    company = html.find("span", {"class":"company"})
    company_anchor = company.a # == company.find('a)
    location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]

    # st has a tag TT
    if company_anchor is None:
        company = str(company.string)
    else:
        company = str(company_anchor.string)
    company = company.strip()
    return {'title':title, 'company':company, 'location':location, "link":f"https://kr.indeed.com/viewjob?jk={job_id}"}

def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&start={page*50}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs
