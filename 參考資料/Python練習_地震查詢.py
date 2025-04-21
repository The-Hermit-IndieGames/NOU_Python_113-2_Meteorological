import requests
from bs4 import BeautifulSoup

url = "https://scweb.cwa.gov.tw/zh-tw/earthquake/limit"
headers = {"User-Agent": "Mozilla/5.0"}

# 發送請求
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 找到「規模大於5.0地震」的區塊 (對應 id="menu2")
section = soup.find("div", id="menu2")

if section:
    # 在該區塊內找到表格
    table = section.find("table")
    rows = table.find_all("tr")[1:]  # 跳過表頭

    earthquakes = []
    for row in rows:
        cols = row.find_all("td")
        time = cols[2].text.strip()  # 時間
        magnitude = float(cols[3].text.strip())  # 規模
        intensity = cols[1].text.strip()  # 震度
        depth = cols[4].text.strip()  # 深度
        location = cols[5].text.strip()  # 位置

        earthquakes.append((time, magnitude,intensity,depth, location))
        if len(earthquakes) >= 5:  # 取前5筆
            break

    # 輸出結果
    for eq in earthquakes:
        print(f"{eq[0]} | 規模: {eq[1]} | 震度: {eq[2]} | 深度: {eq[3]:4s} | 位置: {eq[4]}")
else:
    print("找不到『規模大於5.0地震』區塊")


# 卡結束用
input("輸入任意值結束")