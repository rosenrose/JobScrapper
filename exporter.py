import csv


def save_to_file(filename, jobs):
    with open(filename, "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(list(jobs.values())[0][0].keys())

        for site in jobs:
            for job in jobs[site]:
                writer.writerow(job.values())
    return csv
