from flask import Flask, render_template, request
from werkzeug.utils import escape

app = Flask(__name__)

# 假设的评论数据集
dataset = ["BIT网络安全课程真有趣", "Web安全演示实验打卡", "祝同学们都能取得好成绩!"]

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    if request.method == "POST":
        if request.form.get("submit") == "提交新评论":
            # 通过 escape 函数转义用户输入
            comment = escape(request.form.get("newComment").strip())
            if comment:
                dataset.append(comment)
    elif request.method == "GET":
        if request.args.get("submit") == "提交":
            # 对查询参数进行转义以防止反射型XSS攻击
            query = escape(request.args.get("content").strip())
            if query:
                sub_dataset = [x for x in dataset if query.lower() in x.lower()]
                return render_template("index.html", query=query, comments=sub_dataset)
    # 默认情况下渲染页面，展示所有评论
    return render_template("index.html", query=query, comments=dataset)

if __name__ == "__main__":
    app.run()
