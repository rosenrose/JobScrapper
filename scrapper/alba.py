import os
import csv
import requests
import re
from bs4 import BeautifulSoup

os.system("clear")
os.system("rm *.csv")
alba_url = "https://www.alba.co.kr/"

response = requests.get(alba_url)
soup = BeautifulSoup(response.content, "html.parser", from_encoding="cp949")

superbrand_container = soup.select_one("#MainSuperBrand ul.goodsBox")
superbrand_list = superbrand_container.select("li:not(.noInfo)")
superbrand_info = [
    {
        "company": i.select_one("span.company").text.strip(),
        "link": i.select_one("a")["href"]
    }
    for i in superbrand_list
]

for i, superbrand in enumerate(superbrand_info):
    print(f"{i + 1} / {len(superbrand_info)}", superbrand["company"])

    try:
        response = requests.get(superbrand["link"])
        soup = BeautifulSoup(response.text, "html.parser")
        filename = re.sub(r"[\\/:*?\"<>|]", "_", superbrand["company"])
    except:
        print(superbrand, "error")
        continue

    with open(f"{filename}.csv","w",encoding="utf-8") as file:
        info_table = soup.select_one("#NormalInfo table")
        column_titles = [i.text.strip() for i in info_table.select("thead th")]
        writer = csv.writer(file)
        writer.writerow(column_titles)

        rows = info_table.select("tbody tr:not(.summaryView)")
        for row in rows:
            try:
                place = row.select_one("td.local").text.strip()
                title = row.select_one("td.title span.company").text.strip()
                time = row.select_one("td.data").text.strip()
                pay = row.select_one("td.pay").text.strip()
                date = row.select_one("td.regDate").text.strip()
                writer.writerow([place, title, time, pay, date])
            except:
                print(filename, "error", row)
                file.write(row.text.strip() + "\n")