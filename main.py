####################如要查詢指定餐廳訊息 使用place_id 並可設定他回傳的訊息 例如評論之類
# fields=name,rating,formatted_address,formatted_phone_number,review&
# 使用 nearbysearch 查詢此Location(通常設定經緯度)附近餐廳
#if __name__ == '__main__': #如果XX.py被直接執行的話 __name__ 就會== __main__
    #app.run(debug=True) #如果XX.py被引用到其他的話 import XX.py __name__ 就!= __main__ __main__就不會執行

import mysql.connector
import json
import requests
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
from prettytable import PrettyTable

#透過經緯度來查詢此地點附近餐廳 並存資料 規格是json
#location = '25.01745568776056, 121.40282832703096'
#place_id = 'ChIJJ_TL3nkdaDQRD9Mbj4z0bU0'
#radius = 1000  # 搜索半徑
#types = 'restaurant'  # 餐廳類型
#URL = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?' \
      #f'location={location}&radius={radius}&type=restaurant' \
      #f'&language=zh-TW&key={API_KEY}'

#response = requests.get(URL)
#data = response.json()
#print(json.dumps(data, ensure_ascii=False, indent=4))
class App:
    def register(self, email, name, password):
        connection = self.connect_to_db_user()
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM user WHERE email= %s", (email,))
        result = cursor.fetchone() #只抓取email值

        if email == result[0]: #select from 輸出值為列表[ ] 因此需要[0]因為只有一個值
            print("該email 被註冊")
            # 如使用if result : (這邊只有判斷此email 是否為空值 或 none 沒辦法判斷有沒有重複)
        else:
            cursor.execute("insert into user (email, name, password) values (%s, %s, %s)",(email, name, password))
            connection.commit()
            print("註冊成功")
        cursor.close()
        connection.close()

    def login(self, email, password):
        connection = self.connect_to_db_user()
        cursor = connection.cursor()
        cursor.execute("SELECT email, password from user where email = %s",(email,))
        result = cursor.fetchone()
        if result:
            db_email, db_password = result #解包 result
            if password == db_password:
                print("login 成功")
            else:
                print("密碼錯誤")
        else:
            print("該 email 錯誤 或 尚未被註冊")

    def connect_to_db_user(self):
        return mysql.connector.connect(user='root', password='12345678',
                                       host='127.0.0.1', database='user')




def restaurant_search():
    location = '25.01745568776056, 121.40282832703096'
    radius = 1000
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    print(f"API_KEY: {API_KEY}")
    types = 'restaurant'
    URL = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?' \
          f'location={location}&radius={radius}&types={types}' \
          f'&language=zh-TW&key={API_KEY}'
    response = requests.get(URL)
    data = response.json()
    print(json.dumps(data, ensure_ascii=False, indent=4))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error:{response.status_code}")
        return {}


def connect_to_db():
    return mysql.connector.connect(user='root', password='12345678',
                          host='127.0.0.1', database='what_restaurant')
def insert_restaurant(connection, data):
    cursor = connection.cursor()
    for result in data['results']:
        cursor.execute("insert into choose_restaurant (name, rating, user_ratings_total, address, review) values (%s, %s, %s, %s, %s)",
                       (result.get('name',''),result.get('rating',None),result.get('user_ratings_total',0),result.get('vicinity',None),result.get('review',None))
                       )
    connection.commit()
    cursor.close()
def restaurant_data(connection):
    cursor = connection.cursor()
    cursor.execute("select * from choose_restaurant")
    all_restaurant = cursor.fetchall()
    table = PrettyTable(["id", "Name","rating","user_ratings_total","address","review"])
    for row in all_restaurant:
        table.add_row(row)
    print(table)
    cursor.close()

def main():
    connection = connect_to_db()
    #data = restaurant_search() #因已經有資料 所以暫時不需要從google導入資料
    #insert_restaurant(connection, data) #因已經寫入 所以不需要新的資料
    restaurant_data(connection)
    connection.close()

app = Flask(__name__) #導入模組並引用 模組名稱就是 (__name__) 固定
@app.route("/")
def first():
    return render_template("login,html")

@app.route("/index")
def index():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("select * from choose_restaurant")
    all_restaurant = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html',all_restaurant=all_restaurant)


@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * from choose_restaurant where name like %s or address like %s",(f"%{keyword}%", f"%{keyword}%"))
    search_results = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('search.html', all_restaurant=search_results)

@app.route('/add_review/<int:restaurant_id>', methods=['POST'])
def add_review(restaurant_id):
    new_review = request.form.get('review')
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("UPDATE choose_restaurant SET review = %s WHERE id = %s", (new_review, restaurant_id))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

class Login_function:
    @app.route("/register",methods=['POST','GET'])
    def register(self, email, name, password):
        if request.method == "POST":
            email = request.form.get("email")
            name = request.form.get("name")
            password = request.form.get("password")

            connection = self.connect_to_db_user()
            cursor = connection.cursor()

            cursor.execute("SELECT email FROM user WHERE email= %s", (email,))
            result = cursor.fetchone()  # 只抓取email值]

            if result and email == result[0]:  # select from 輸出值為列表[ ] 因此需要[0]因為只有一個值
                print("該email 被註冊")
                # 如使用if result : (這邊只有判斷此email 是否為空值 或 none 沒辦法判斷有沒有重複)
            else:
                cursor.execute("insert into user (email, name, password) values (%s, %s, %s)", (email, name, password))
                connection.commit()
                print("註冊成功")
                cursor.close()
                connection.close()
                return redirect(url_for("login"))

    @app.route("/Login",methods=['POST','GET'])
    def login(self, email, password):
        connection = self.connect_to_db_user()
        cursor = connection.cursor()
        cursor.execute("SELECT email, password from user where email = %s", (email,))
        result = cursor.fetchone()
        if result:
            db_email, db_password = result  # 解包 result
            if password == db_password:
                print("login 成功")
            else:
                print("密碼錯誤")
        else:
            print("該 email 錯誤 或 尚未被註冊")

    def connect_to_db_user(self):
        return mysql.connector.connect(user='root', password='12345678',
                                       host='127.0.0.1', database='user')






###############################################################
#for result in data['results']: #因第一次執行將api吐出資訊導入到SQL後 不需要再次寫入
    #cursor.execute(
        #"insert into choose_restaurant (name, rating, user_ratings_total, address) values(%s, %s, %s, %s)",
        #(result['name'],result.get('rating',None),
        #result.get('user_ratings_total',0),result.get('vicinity',None))
    #)
    #print(f"Inserting {data['results'][0]['name']} into database")
################################################################
##顯示全部資料表整理成表格
#cursor.execute("select * from choose_restaurant")
#all_restaurant = cursor.fetchall()
#table = PrettyTable(["id","Name","rating","user_ratings_total","address"])
#for row in all_restaurant:
    #table.add_row(row)
#print(table)
#####################################################################
#cursor = connection.cursor()  # 呼叫說要使用
#connection.commit() #提交並上傳資料
#cursor.close() #告訴資料庫先不用使用
#connection.close() # 將資料庫關起來












