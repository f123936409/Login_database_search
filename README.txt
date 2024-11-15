#import mysql.connector
#import json
#import requests
#from flask import Flask, render_template, request, redirect, url_for
#from dotenv import load_dotenv
#import os
#from prettytable import PrettyTable
上述使用的模組
#練習專案內容 使用google API 查詢附近餐廳後 存到資料庫內 並可以從資料庫抓資料並修改其內容
#如需使用google API功能 需自備google API金鑰
#新增用戶登入 註冊功能 需先註冊後登入 使用查詢餐廳功能