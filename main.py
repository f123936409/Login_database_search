<<<<<<< HEAD
####################如要查詢指定餐廳訊息 使用place_id 並可設定他回傳的訊息 例如評論之類
# fields=name,rating,formatted_address,formatted_phone_number,review&
# 使用 nearbysearch 查詢此Location(通常設定經緯度)附近餐廳
#if __name__ == '__main__': #如果XX.py被直接執行的話 __name__ 就會== __main__
    #app.run(debug=True) #如果XX.py被引用到其他的話 import XX.py __name__ 就!= __main__ __main__就不會執行
#request 要先有發起[POST][GET]才能使用   requests 是構造pest get一起使用的
#app.config 是 Flask 提供的配置存儲空間。
import mysql.connector
import json
import requests
from flask import Flask, render_template, request, redirect, url_for ,jsonify
from dotenv import load_dotenv
import os
from prettytable import PrettyTable
from flask_jwt_extended import JWTManager ,jwt_required , get_jwt_identity
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash ,check_password_hash

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
class App1111:#並未與html連動 須在外部給予email name password 值做呼叫
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
            return redirect(url_for("login"))

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



class googleAPI:
    def restaurant_search(self):
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
        if response.status_code == 200:
            connection = self.connect_to_db()
            self.insert_restaurant(connection, data)
            #return response.json()
        else:
            print(f"Error:{response.status_code}")
            return {}

    def restaurant_detail(self):
        load_dotenv()
        API_KEY=os.getenv("API_KEY")
        place_id = '123'
        URL = f'https://maps.googleapis.com/maps/api/place/details/json?' \
              f'place_id={place_id}' \
              f'&language=zh-TW&key={API_KEY}'
        response = requests.get(URL)
        data = response.json()

    def connect_to_db(self):
        return mysql.connector.connect(user='root', password='12345678',
                              host='127.0.0.1', database='what_restaurant')

    def insert_restaurant(self,connection, data):
        cursor = connection.cursor()
        for result in data['results']:
            cursor.execute("insert into choose_restaurant (name, rating, user_ratings_total, address, review, place_id) values (%s, %s, %s, %s, %s, %s)",
                           (result.get('name',''),result.get('rating',None),result.get('user_ratings_total',0),result.get('vicinity',None),result.get('review',None),
                            result.get('place_id',None))
                           )
        connection.commit()
        cursor.close()

    def restaurant_data(self,connection):
        cursor = connection.cursor()
        cursor.execute("select * from choose_restaurant")
        all_restaurant = cursor.fetchall()
        table = PrettyTable(["id", "Name","rating","user_ratings_total","address","review","place_id"])
        for row in all_restaurant:
            table.add_row(row)
        print(table)
        cursor.close()
#if __name__ == '__main__':
    #api = googleAPI()
    #api.connect_to_db()
    #api.restaurant_search()


    #def main(self):
        #connection = self.connect_to_db
        #data = self.restaurant_search() #因已經有資料 所以暫時不需要從google導入資料
        #insert_restaurant(,connection, data) #因已經寫入 所以不需要新的資料
        #restaurant_data(connection)
        #connection.close()

app = Flask(__name__) #導入模組並引用 模組名稱就是 (__name__) 固定
print(1)
load_dotenv()
print(2)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") #設定secret_key
print(3)
jwt = JWTManager(app) #實體化jwt加密功能
print(4)

class dataSearch:
    def __init__(self,app):
        print(5)
        self.app = app
        self.app.add_url_rule('/',view_func=self.first)
        self.app.add_url_rule('/profile/index',view_func=self.index)
        self.app.add_url_rule('/profile/search',view_func=self.search,methods=['POST'])
        self.app.add_url_rule('/profile/add_review/<int:restaurant_id>',view_func=self.add_review,methods=['POST'])
    #@app.route("/")
    def first(self):
        return render_template("frontpage.html")

    #@app.route("/index")
    @jwt_required(locations=["cookies"])
    def index(self):
        connection = self.connect_to_db()
        cursor = connection.cursor()
        cursor.execute("select * from choose_restaurant")
        all_restaurant = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('index.html',all_restaurant=all_restaurant)


    #@app.route('/search', methods=['POST'])
    def search(self):
        keyword = request.form.get('keyword')
        connection = self.connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * from choose_restaurant where name like %s or address like %s",(f"%{keyword}%", f"%{keyword}%"))
        search_results = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('search.html', all_restaurant=search_results)

    #@app.route('/add_review/<int:restaurant_id>', methods=['POST'])
    @jwt_required(locations=["cookies"])
    def add_review(self,restaurant_id):
        new_review = request.form.get('review')
        connection = self.connect_to_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE choose_restaurant SET review = %s WHERE id = %s", (new_review, restaurant_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))

    def connect_to_db(self):
        return mysql.connector.connect(user='root', password='12345678',
                                       host='127.0.0.1', database='what_restaurant')



class Login_function:
    def __init__(self,app):
        print(6)
        self.app = app
        #JWT配置
        self.app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
        self.app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"  # 設定為存入的 Cookie 名稱
        self.app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # 替換為你的密鑰
        self.jwt = JWTManager(self.app)

        #URL規則
        self.app.add_url_rule('/guest/register',view_func=self.register,methods=['POST','GET'])
        self.app.add_url_rule('/guest/login',view_func=self.login,methods=['POST','GET'])
        self.app.add_url_rule('/error',view_func=self.error_page,methods=['GET'])
        self.app.add_url_rule('/profile',view_func=self.profile,methods=['GET'])
        #self.app.add_url_rule('/frontpage',view_func=self.guest,methods=['GET'])

    #@app.route("/register",methods=['POST','GET'])
#app.route 內容= self.add_url_rule('/',endpoint='',view_func=只需要寫函數名稱不能+(),methods)

    def error_page(self):
        return render_template(('error.html'))

    def register(self):
        if request.method == "POST":
            email = request.form.get("email")
            name = request.form.get("name")
            password = request.form.get("password")
            if not email or not name or not password:
                print("所有欄位都必須填寫")
                return render_template("register.html", message="所有欄位必須填寫")
            hash_password = generate_password_hash(password)#密碼加密
            print(f"Email: {email}, Name: {name}, Password: {password}")
            try:
                connection = self.connect_to_db_user()
                cursor = connection.cursor()

                cursor.execute("SELECT email FROM user WHERE email= %s", (email,))
                result = cursor.fetchone()  # 只抓取email值]

                if result :  # select from 輸出值為列表[ ] 因此需要[0]因為只有一個值
                    print("該email 被註冊或不能為空白")
                    return render_template("register.html", message="該email 已經被註冊")
                    # 如使用if result : (這邊只有判斷此email 是否為空值 或 none 沒辦法判斷有沒有重複)
                else:
                    cursor.execute("insert into user (email, name, password) values (%s, %s, %s)", (email, name, hash_password))
                    connection.commit()
                    print("註冊成功")
                    return redirect(url_for("login",message="註冊成功"))

            except Exception as e:
                print(f"發生錯誤: {e}")
                return render_template("register.html", message="註冊過程中出現錯誤")  # 顯示錯誤訊息

            finally:
                cursor.close()
                connection.close()

        elif request.method == "GET":
                return render_template("register.html")

    #@app.route("/login",methods=['POST','GET'])
    def login(self):
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            if not email or not password:
                print("email or 密碼未填寫")
                return redirect(url_for('login'))
            try:
                connection = self.connect_to_db_user()
                cursor = connection.cursor()
                cursor.execute("SELECT name, password from user where email = %s", (email,))
                result = cursor.fetchone()

                if result :
                    db_name, db_password = result  # 解包 result
                    if check_password_hash(db_password,password):
                        print("登入成功") #登入成功後將創建的token存至cookies
                        access_token = create_access_token(identity=db_name)#(JWT驗證)建立access_token
                        response = redirect(url_for("profile",user_id=db_name))
                        response.set_cookie("access_token", access_token)#(JWT驗證)將access_token存到cookie
                        return response
                    else:
                        print("密碼錯誤")
                        return redirect(url_for("error_page"))
                else:
                    print("該 email 錯誤 或 尚未被註冊")
                    return redirect(url_for('error_page'))
            finally:
                cursor.close()
                connection.close()
        elif request.method == "GET":
                return render_template("login.html")

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return redirect(url_for('login', message="Token 過期，請重新登入"))

    @jwt_required(locations=["cookies"])  # 從 Cookie 中驗證
    def profile(self):
        user_id = get_jwt_identity()
        if not user_id:
            return redirect(url_for('/profile/login'))
        return render_template('Profile.html', db_name=user_id)

    #def guest(self):
        #return redirect(url_for('frontpage'))

    def connect_to_db_user(self):
        return mysql.connector.connect(user='root', password='12345678',
                                       host='127.0.0.1', database='user')

print(7)
login_function = Login_function(app)
print(8)
data_search = dataSearch(app)

if __name__ == '__main__':
    app.run(debug=True)



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












=======
from flask import Flask, render_template ,request , redirect ,url_for ,jsonify
import os

class page:
    def __init__(self,app):
        self.app = app
        self.app.add_url_rule('/',view_func=self.guest)

    def guest(self):
        return render_template("Home.html")

app = Flask(__name__)
page = page(app)
if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 058e33c3f815aa0c2c8f2aeafa602c0c505b4313
