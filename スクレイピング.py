from bs4 import BeautifulSoup
import requests #HTTP操作用
# アクセスしたいWebサイトのURL
url = 'https://www.toshin.com/weather/detail?id=61759'

# Webサーバにリクエストを出す．レスポンスを変数に格納しておく
r = requeｓts.get(url)
print(r)
print(f'リクエスト：{r.request}') # 自分の出したリクエスト情報
print(f'リクエストヘッダー：{r.request.headers}') # リクエストヘッダー

print(f'HTTPステータスコード：{r.status_code}') # HTTPステータスコード
print(f'HTTPステータスメッセージ：{r.reason}') # HTTPステータスメッセージ

print(f'レスポンスヘッダー：{r.headers}') # レスポンスヘッダー
print(f'レスポンスのコンテンツ：{r.text}') # コンテンツ（HTMLソース）
url = 'https://www.toshin.com/weather/detail?id=61759'

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
elems = soup.select('#weather_box3_1 > div > table > tbody > tr:nth-of-type(5)') 
elems2 = soup.select('#weather_box3_1 > div > table > tbody > tr:nth-of-type(1)')     
cell_texts2 = [cell.get_text(strip=True) for cell in elems2[0].find_all('td')]
cell_texts = [cell.get_text(strip=True) for cell in elems[0].find_all('td')]

con = sqlite3.connect('weather_data.db')
cur = con.cursor()
sql_create_table_cars = 'CREATE TABLE climate_table(id INTEGER PRIMARY KEY AUTOINCREMENT, time text, hu int);'
cur.execute(sql_create_table_cars)
con.commit()
con.close()

def insert_data(date,hu):
    con = sqlite3.connect('weather_data.db')
    cur = con.cursor()
    sql = f"INSERT INTO climate_table (time , hu) VALUES (?,?)"
    data_list = [date,hu]
    cur.execute(sql, data_list)
    con.commit()
    con.close()

    elems = soup.select('#weather_box3_1 > div > table > tbody > tr:nth-of-type(5)')  
elems2 = soup.select('#weather_box3_1 > div > table > tbody > tr:nth-of-type(1)')   
date_list = [cell.get_text(strip=True) for cell in elems2[0].find_all('td')]
hu_list = [cell.get_text(strip=True) for cell in elems[0].find_all('td')]

def insert_data_all(date_list, hu_list):
    for i in range(len(date_list)):
        insert_data(date_list[i], hu_list[i])

insert_data_all(date_list, hu_list)

con = sqlite3.connect('weather_data.db')
cur = con.cursor()
sql_create_table = 'CREATE TABLE local_data_table(id INTEGER PRIMARY KEY AUTOINCREMENT, time text, hu int);'
cur.execute(sql_create_table)
con.commit()
con.close()

def insert_data2(date,hu):
    con = sqlite3.connect('weather_data.db')
    cur = con.cursor()
    sql = f"INSERT INTO local_data_table (time , hu) VALUES (?,?)"
    data_list = [date,hu]
    cur.execute(sql, data_list)
    con.commit()
    con.close()

insert_data2('0時',45)
insert_data2('1時',47)
insert_data2('2時',46)
insert_data2('3時',46)
insert_data2('4時',46)
insert_data2('5時',45)
insert_data2('6時',45)
insert_data2('7時',47)
insert_data2('8時',49)
insert_data2('9時',43)
insert_data2('10時',44)
insert_data2('11時',41)
insert_data2('12時',45)
insert_data2('13時',47)
insert_data2('14時',43)
insert_data2('15時',44)
insert_data2('16時',46)
insert_data2('17時',47)
insert_data2('18時',47)
insert_data2('19時',58)
insert_data2('20時',55)
insert_data2('21時',49)
insert_data2('22時',47)
insert_data2('23時',45)

import sqlite3
import matplotlib.pyplot as plt

# データベースからデータを取得する関数
def fetch_data_from_db(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f'SELECT time, hu FROM {table_name}')
    data = cur.fetchall()
    conn.close()
    return data

# データベースからデータを取得
data_table1 = fetch_data_from_db('weather_data.db', 'climate_table')
data_table2 = fetch_data_from_db('weather_data.db', 'local_data_table')

# グラフの作成
timestamps_table1, temperatures_table1 = zip(*data_table1)
timestamps_table2, temperatures_table2 = zip(*data_table2)

plt.plot(timestamps_table1, temperatures_table1, label='climate_table')
plt.plot(timestamps_table2, temperatures_table2, label='local_data_table')

plt.xlabel('Time')
plt.ylabel('Humidity')
plt.title('Comparison of Humidity between climate_table and local_data_table')
plt.legend()
plt.show()
