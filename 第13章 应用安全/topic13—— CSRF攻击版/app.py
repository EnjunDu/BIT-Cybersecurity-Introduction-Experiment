from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

dataset=["BIT网络安全课程真有   趣","Web安全演示实验打卡","祝同学们都能取得好成绩!"]


@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    if request.method == "POST":
        if request.form.get("submit") == "提交新评论":
            comment = request.form.get("newComment").strip()
            print(type(comment))
            if comment:
                dataset.append(comment)
    elif request.method == "GET":
        if request.args.get("submit") == "提交":
            query = request.args.get("content").strip()
            if query:
                sub_dataset = [x for x in dataset if query in x]
                return render_template("index.html", query=query, comments=sub_dataset)
    return render_template("index.html", query=query, comments=dataset)


if __name__ == "__main__":
    app.run()