from flask import Flask, render_template, redirect, request
import sys

from flask.helpers import url_for
sys.path.append(".")
from student_manage import app_config
from student_manage import database
import datetime


app = Flask(__name__)
app.config.from_object(app_config)


@app.route('/')
def student_manage():
    db = database.Mysqls()
    # 性别
    sex = {"1": "男", "0": "女"}
    student_info = db.get_all("""
                              select s.id, s.name, sex, age, birthday, m.name, instructor, institute
                              from student s join major m on s.major_id = m.id where s.date_delete is null and m.date_delete is null
                              """)
    for item in student_info:
        try:
            item["sex"] = sex[item["sex"]]
        except Exception:
            pass
    # 字段名
    field = ["学号", "姓名", "性别", "年龄", "出生日期", "专业", "指导员", "学院"]
    # title
    title = "学生"
    return render_template('show.html', info=student_info, field=field, title=title)


@app.route('/major')
def major_manage():
    db = database.Mysqls()
    student_info = db.get_all("""
                              SELECT id, name, instructor, institute FROM major WHERE date_delete is null
                              """)
    # 字段名
    field = ["专业代码", "专业名称", "指导老师", "学院"]
    # title
    title = "专业"
    return render_template('show.html', info=student_info, field=field, title=title)


@app.route('/remove_student/<int:id>')
def remove_student(id):
    # 获取当前时间
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = database.Mysqls()
    db.remove("""
              update student set date_delete = "{0}" where id={1}
              """.format(time, id))
    return redirect(url_for("student_manage"))


@app.route('/remove_major')
def remove_major():
    is_delete = False
    # 获取当前时间
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = database.Mysqls()
    id = request.args.get("major_id")
    # 判断专业下是否有学生
    is_student = db.get_all("select 1 from student where major_id='{0}' and date_delete is null limit 1".format(id))
    sql_string = "update major set date_delete ='{0}' where id={1}".format(time, id)
    if not is_student:
        is_delete = db.remove(sql_string)
    return {"code": 200, "succes": is_delete}


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    db = database.Mysqls()
    # title
    title = "添加学生"
    if request.method == "GET":
        major_info = db.get_all("""
                              SELECT id, name, instructor, institute FROM major WHERE date_delete is null
                              """)
        return render_template("add_student.html", major=major_info, title=title)
    if request.method == "POST":
        name = request.form.get("student_name")
        sex = request.form.get("student_sex")
        major = request.form.get("student_major")
        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 年龄
        age = int(time.split("-")[0]) - int(year)
        birth = year + "-" + month + "-" + day
        is_student = db.get_all("select * from student where name='{0}' and date_delete is not null and sex='{1}' and birthday='{2}' limit 1".format(name, sex, birth))
        if is_student:
            db.update("""
                      update student set date_delete=NULL, date_update='{0}', age='{1}', major_id='{2}' where id={3}
                      """.format(time, age, major, is_student[0]["id"]))
        else:
            db.add_one("""
                   INSERT INTO student(name, sex, age, birthday , major_id, date_create, date_update, date_delete) VALUES ("{0}", "{1}", "{2}",  "{3}",  "{4}", "{5}", "{5}", NULL);
                   """.format(name, sex, age, birth, major, time))
        return redirect(url_for("student_manage"))


@app.route('/add_major', methods=['GET', 'POST'])
def add_major():
    db = database.Mysqls()
    # title
    title = "添加专业"
    if request.method == "GET":
        return render_template("add_major.html", title=title)
    if request.method == "POST":
        name = request.form.get("major_name")
        adviser = request.form.get("adviser")
        student_name = request.form.get("student_name")
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        is_major = db.get_all("select * from major where name='{0}' and date_delete is not null and instructor='{1}' and institute='{2}' limit 1".format(name, adviser, student_name))
        if is_major:
            db.update("""
                      update major set date_delete=NULL, date_update='{0}' where id={1}
                      """.format(time, is_major[0]["id"]))
        else:
            db.add_one("""
                    INSERT INTO major(name, instructor, institute, date_create, date_update, date_delete) VALUES ("{0}", "{1}", "{2}",  "{3}",  "{3}", NULL);
                    """.format(name, adviser, student_name, time))
        return redirect(url_for("major_manage"))


@app.route('/update_major', methods=['GET', 'POST'])
def update_major():
    db = database.Mysqls()
    if request.method == "GET":
        id = request.args.get("major_id")
        sql_string = "select * from major where id={0} and date_delete is null".format(id)
        major_info = db.get_all(sql_string)
        return major_info[0]
    if request.method == "POST":
        major_id = request.form.get("major_id")
        name = request.form.get("major_name")
        adviser = request.form.get("adviser")
        student_name = request.form.get("student_name")
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.update("""
                  update major set name='{0}', instructor='{1}', institute='{2}', date_update='{3}' where id={4}
                  """.format(name, adviser, student_name, time, major_id))
        return redirect(url_for("major_manage"))


@app.route('/update_student', methods=['GET', 'POST'])
def update_student():
    db = database.Mysqls()
    if request.method == "GET":
        id = request.args.get("major_id")
        major_info = db.get_all("""
                              SELECT id, name, instructor, institute FROM major WHERE date_delete is null
                              """)
        sql_string = "select * from student where id={0} and date_delete is null".format(id)
        student_info = db.get_all(sql_string)
        student_info = student_info[0]
        student_info["birthday"] = student_info["birthday"].strftime('%Y-%m-%d')
        return {"major": major_info, "student": student_info}
    if request.method == "POST":
        student_id = request.form.get("student_id")
        name = request.form.get("student_name")
        sex = request.form.get("student_sex")
        major = request.form.get("student_major")
        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 年龄
        age = int(time.split("-")[0]) - int(year)
        # 出生日期
        birth = year + "-" + month + "-" + day
        print(birth)
        db.update("""
                  update student set date_update='{0}', age='{1}', major_id='{2}', birthday='{3}', name='{4}', sex='{5}' where id={6}
                  """.format(time, age, major, birth, name, sex, student_id))
        return redirect(url_for("student_manage"))


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
