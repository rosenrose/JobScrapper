import csv


def save_to_csv(filename: str, jobs: list[dict[str, str]]):
    with open(filename, "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([i[0].upper() + i[1:] for i in jobs[0].keys()])

        for job in jobs:
            writer.writerow(job.values())
