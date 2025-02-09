from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fan_xing_yu_is_little_boy_mother'
csrf = CSRFProtect(app)

# 定义评论表单类
class CommentForm(FlaskForm):
    newComment = StringField('评论')
    submit = SubmitField('提交新评论')

dataset = ["BIT网络安全课程真有趣", "Web安全演示实验打卡", "祝同学们都能取得好成绩!"]

@app.route("/", methods=["GET", "POST"])
def index():
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.newComment.data.strip()
        if comment:
            dataset.append(comment)
        return redirect(url_for('index'))
    query = request.args.get('content', '')
    sub_dataset = [x for x in dataset if query.lower() in x.lower()]
    return render_template("index.html", form=form, comments=sub_dataset, query=query)

if __name__ == "__main__":
    app.run(debug=True)
