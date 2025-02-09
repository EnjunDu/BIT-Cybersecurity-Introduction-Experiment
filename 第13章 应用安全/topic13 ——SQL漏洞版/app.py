from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.utils import escape

app = Flask(__name__)
app.secret_key = 'fan_xing_yu_is_little_boy_mother'

# 假设的评论数据集
dataset = ["BIT网络安全课程真有趣", "Web安全演示实验打卡", "祝同学们都能取得好成绩!"]

# 注册功能
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['newUsername']
        new_password = request.form['newPassword']
        connection = sqlite3.connect('login.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
        connection.commit()
        connection.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get('logged_in'):  # 检查用户是否登录
        return redirect(url_for('login'))  # 未登录，重定向到登录页面
    query = ""
    if request.method == "POST":
        if request.form.get("submit") == "提交新评论":
            comment = escape(request.form.get("newComment").strip())
            if comment:
                dataset.append(comment)
    elif request.method == "GET":
        if request.args.get("submit") == "提交":
            query = escape(request.args.get("content").strip())
            if query:
                sub_dataset = [x for x in dataset if query.lower() in x.lower()]
                return render_template("index.html", query=query, comments=sub_dataset)
    return render_template("index.html", query=query, comments=dataset)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # 从表单中获取用户名和密码
        username = request.form['username']
        password = request.form['password']
        connection = sqlite3.connect('login.db')
        cursor = connection.cursor()

        # 故意引入 SQL 注入的隐患（仅作为演示，实际中不应这么做）
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)

        user = cursor.fetchone()
        connection.close()
        if user:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = "Invalid username or password"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
