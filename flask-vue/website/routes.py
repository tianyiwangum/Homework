import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
load_dotenv()

from flask import Flask,render_template,url_for,flash,redirect,request
from website.forms import RegistrationForm,LoginForm,Account,Stock
from website.models import add_to_database,UserModel
from website import app,db, bcrypt
from flask_login import login_user,current_user,logout_user,login_required
# from flask_mail import Message
import secrets
from PIL import Image
import pdfkit


stock_id_lists = {
    '000001.SZ':'static\\a.csv',
    '002371.SZ':'static\\b.csv',
    'AAPL':'static\\c.csv'
}



def handle_exception(e):
    """Handle exception"""
    return redirect(url_for("error"),code=301)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,ext = os.path.splitext(form_picture.filename)
    pic = random_hex + ext
    path = os.path.join(app.root_path,'static/profiles',pic)
    output_size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(path)
    return pic


title = "Posts"

@app.route("/")
def hello():
    return render_template("home.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello'),code=301)
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = UserModel(username=form.username.data,email=form.email.data,password=hashed)
        add_to_database(new_user)
        return redirect(url_for('login'),code=302)
    return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello'),code=301)
    form = LoginForm()
    if form.validate_on_submit():
        try:
            logged = UserModel.find_by_email(form.email.data)
            if logged and bcrypt.check_password_hash(logged.password,form.password.data):
                login_user(logged,remember=form.remember.data)
                next_page = request.args.get('next')            
                if next_page:
                    return redirect(next_page,code=302)
                else:
                    return redirect(url_for('hello'),code=301)
            else:
                flash('Login unsuccessful')
        except Exception as e:
            handle_exception(e)
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("hello"),code=302)


@app.route("/accounts",methods=['GET','POST'])
@login_required  #checks if user logged in or not and then allows access
def accounts():
    form= Account()
    if form.validate_on_submit():
        try:
            current_user.username = form.new_username.data
            current_user.email = form.new_email.data  # Update current user values
            db.session.commit()
            flash("Your Account has been updated","success")
        except Exception as e:
            handle_exception(e)
        return redirect(url_for("accounts"),code=301)
    elif request.method == 'GET':
        form.new_username.data = current_user.username
        form.new_email.data = current_user.email
    return render_template("accounts.html",title="Account",form=form)


@app.route('/stock_selector', methods=['GET','POST'])
@login_required
def stocks_selector():
    form = Stock();
    if form.validate_on_submit():
        if form.stock_id in stock_id_lists:
            cur_stock = stock_id_lists[form.stock_id]
        return redirect(url_for("stocks_vis"), code=301)
    return render_template("stock_select.html", form=form, title="Stock Selector")

@app.route("/stocks_vis",methods=['GET','POST'])
@login_required  #checks if user logged in or not and then allows access
def visualize_stocks():
    form = Stock()
    cur_stock = os.path.join(app.root_path,'static\\a.csv')
    if form.validate_on_submit():
        if form.stock_id in stock_id_lists:
            cur_stock = os.path.join(app.root_path,stock_id_lists[form.stock_id])
            
        df = pd.read_csv(cur_stock, parse_dates=['trade_date'])
        start_date = form.start_date.data
        end_date = form.end_date.data
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        index = form.index.data
        mask = ((df['trade_date'] >= start_date) & (df['trade_date'] <= end_date))
        data = df.loc[mask]
        data.sort_values(by='trade_date', ascending=True)
        # 从 DataFrame 中提取需要的数据
        x_data = data['trade_date'].tolist()
        y_data = data[index].tolist()
        # 生成 ECharts 图表所需的数据格式
        series_data = []
        for y in y_data:
            series_data.append({'value': y})

        # 构建 ECharts 图表的配置项
        option = {
            'xAxis': {'type': 'category', 'data': x_data},
            'yAxis': {'type': 'value'},
            'series': [{'type': 'line', 'data': series_data}]
        }
        return render_template("vis.html", title='Visualize', form=form ,option=option, name=current_user.username)
    
    df = pd.read_csv(cur_stock, parse_dates=['trade_date'])
    start_date = '2022-01-22'
    end_date = '2022-12-01'
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    index = 'close'
    mask = ((df['trade_date'] >= start_date) & (df['trade_date'] <= end_date))
    data = df.loc[mask]
    data.sort_values(by='trade_date', ascending=True)
    # 从 DataFrame 中提取需要的数据
    x_data = data['trade_date'].tolist()
    y_data = data[index].tolist()
    # 生成 ECharts 图表所需的数据格式
    series_data = []
    for y in y_data:
        series_data.append({'value': y})
    # 构建 ECharts 图表的配置项
    option = {
        'xAxis': {'type': 'category', 'data': x_data},
        'yAxis': {'type': 'value'},
        'series': [{'type': 'line', 'data': series_data}]
    }
    return render_template("vis.html", title='Visualize', form=form, option=option, name=current_user.username)
    