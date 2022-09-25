import csv
from extractors import wwr, indeed
from typing import Final, List, Dict

USER_AGENT: Final = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"


def save_csv(filename: str, jobs: List[Dict[str, str]]):
    with open(filename, "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([i[0].upper() + i[1:] for i in jobs[0].keys()])

        for job in jobs:
            writer.writerow(job.values())


def main():
    query = input("term: ")

    wwr_results = wwr.extract_jobs(query, USER_AGENT)
    indeed_results = indeed.extract_jobs(query, USER_AGENT)
    # print(*indeed_results, sep="\n")
    save_csv("jobs.csv", wwr_results + indeed_results)


if __name__ == "__main__":
    main()
