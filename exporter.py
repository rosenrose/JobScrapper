import csv

def save_to_file(filename, jobs):
    with open(filename, "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(jobs[0].keys())

        for job in jobs:
            writer.writerow(job.values())
    return csv