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
