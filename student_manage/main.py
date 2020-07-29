from flask import Flask, render_template
import sys
sys.path.append(".")
from student_manage import app_config
from student_manage import database


app = Flask(__name__)
app.config.from_object(app_config)


@app.route('/')
def student_manage():
    db = database.Mysqls()
    student_info = db.get_all("""
                              select s.id, s.name, sex, age, birthday, m.name, instructor, institute
                              from student s join major m on s.major_id = m.id where s.date_delete is null and m.date_delete is null
                              """)
    # 字段名
    field = ["学号", "姓名", "性别", "年龄", "出生日期", "专业", "指导员", "学院"]
    return render_template('show.html', info=student_info, field=field)


@app.route('/major')
def major_manage():
    return render_template('show.html', name="张三")


@app.route('/login')
def login():
    return render_template('show.html', name="张三")


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
