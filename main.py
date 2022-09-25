from extractors import wwr, indeed
from typing import Final

USER_AGENT: Final = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"


def main():
    query = input("term: ")

    # wwr_results = wwr.extract_jobs(query)
    indeed_results = indeed.extract_jobs(query, USER_AGENT)
    print(*indeed_results, sep="\n")


if __name__ == "__main__":
    main()
