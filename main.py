import pandas as pd
from bs4 import BeautifulSoup
import time
import urllib.request
ADJUST_ZERO_PRICE = True
BUY_NEW = True


def parse_series(s: pd.Series) -> tuple[str, str, str, str] | None:
    if not s.isnull().values.any():
        return (s["BLItemNo"], str(int(s["BLColorId"])),
                s["ColorName"], str(int(s["Qty"])))
    else:
        pass

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


def response_to_avg_price(response: str) -> tuple[str, float]:
    avg = [i for i in response.split(" ") if "Avg" in i and "Price" in i][0]
    avg = avg.replace("Price:", "").replace("Avg", "").split(u'\xa0')
    return (avg[0], float(avg[1]))


def request_price(s: pd.Series):
    code, color, color_name, amount = (s["code"], s["color"],
                                       s["color_name"], s["amount"])
    amount = int(amount)
    link = f"https://www.bricklink.com/catalogPG.asp?P={code}&ColorID={color}"
    print(link)
    opener = AppURLopener()
    response = opener.open(link)
    html = response.read()
    soup = BeautifulSoup(html, features="lxml")
    tables = soup.find_all("table", {"class": "fv"})
    new, used = map(lambda x: x.text, tables[1:3])
    if BUY_NEW:
        response = new
    else:
        response = used
    with open("data.txt", "a") as file:
        currency, price = response_to_avg_price(response)
        if not price and ADJUST_ZERO_PRICE:
            price = 0.01
        file.write(f"{amount}x {color_name} {code} {price*amount} {currency}\n")
    time.sleep(10)


def parse_details(path: str) -> None:
    df = pd.read_csv(path)
    s = df.apply(parse_series, axis=1).dropna()
    df = pd.DataFrame(s, columns = ["main"])
    columns = ["code", "color", "color_name", "amount"]
    for i, name in enumerate(columns):
        df[name] = [val[i] for val in df["main"]]
    df = df[columns]
    with open("data.txt", "w") as file:
        pass
    df.apply(request_price, axis=1)


def file_to_human(df_path: str, file_path: str) -> None:
    pass

def main():
    parse_details("example-tiny.csv")


if __name__ == "__main__":
    main()