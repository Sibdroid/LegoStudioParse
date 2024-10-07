import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import urllib.request


def parse_series(s: pd.Series) -> tuple[int, str, str] | None:
    if not s.isnull().values.any():
        return s["BLItemNo"], str(int(s["BLColorId"])), str(int(s["Qty"]))
    else:
        pass

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


def request_price(s: pd.Series) -> str:
    code, color = s["code"], s["color"]
    link = f"https://www.bricklink.com/catalogPG.asp?P={code}&ColorID={color}"
    print(link)
    opener = AppURLopener()
    response = opener.open(link)
    html = response.read()
    soup = BeautifulSoup(html, features="lxml")
    tables = soup.find_all("table", {"class": "fv"})
    new, used = map(lambda x: x.text, tables[1:3])
    with open("data.txt", "a") as file:
        file.write(new+"\n")
        file.write("\n")
        print("done")
    time.sleep(10)


def parse_details(path: str) -> None:
    df = pd.read_csv(path)
    s = df.apply(parse_series, axis=1).dropna()
    df = pd.DataFrame(s, columns = ["main"])
    columns = ["code", "color", "amount"]
    for i, name in enumerate(columns):
        df[name] = [val[i] for val in df["main"]]
    df = df[columns]
    with open("data.txt", "w") as file:
        pass
    df.apply(request_price, axis=1)


def file_to_human(df_path: str, file_path: str) -> None:
    pass

def main():
    #parse_details("example-tiny.csv")
    pass


if __name__ == "__main__":
    main()