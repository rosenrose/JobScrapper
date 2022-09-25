import csv
import json
from io import StringIO, BytesIO


def save_to_csv(jobs: list[dict[str, str]]) -> BytesIO:
    with StringIO() as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([i[0].upper() + i[1:] for i in jobs[0].keys()])

        for job in jobs:
            writer.writerow(job.values())

        output = BytesIO(csv_file.getvalue().encode("utf-8"))

    return output


def save_to_json(jobs: list[dict[str, str]]) -> BytesIO:
    json_string = json.dumps(jobs, ensure_ascii=False, indent=2)

    return BytesIO(json_string.encode("utf-8"))
