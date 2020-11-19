from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, DataRequired
from flask_mysqldb import MySQL
import backup



app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'abonitalla123'
app.config['MYSQL_DB'] = 'studentdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
Bootstrap(app)


class RegisterForm(FlaskForm):
    firstname = StringField('Firstname', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])
    studentid = StringField('StudentID', validators=[InputRequired()])
    year = StringField('Year', validators=[InputRequired()])
    choice1 = backup.coursecount()
    field1 = SelectField(u'Course', choices=choice1, validators=[DataRequired()])
    choice2 = backup.departmentcount()
    field2 = SelectField(u'Department', choices=choice2, validators=[DataRequired()])
    choice3 = backup.collegecount()
    field3 = SelectField(u'Colleges', choices=choice3, validators=[DataRequired()])


class CollegeForm(FlaskForm):
    number = StringField("No.", validators=[InputRequired()])
    code = StringField('Code', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])

class CourseForm(FlaskForm):
    number = StringField("No.", validators=[InputRequired()])
    code = StringField('Code', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    myChoices = backup.collegecount()
    myField = SelectField(u'Colleges', choices=myChoices, validators=[DataRequired()])


class DepartmentForm(FlaskForm):
    number = StringField("No.", validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    myChoices = backup.collegecount()
    myField = SelectField(u'Colleges', choices=myChoices, validators=[DataRequired()])


class Searchform(FlaskForm):
    studentid = StringField('Student ID', validators=[InputRequired()])


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/students', methods=['GET'])
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    studentdetails = cur.fetchall()
    return render_template('students.html', studentdetails=studentdetails)


@app.route('/college', methods=['GET'])
def college():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM college")
    collegedetails = cur.fetchall()
    return render_template('college.html', collegedetails=collegedetails)


@app.route('/course', methods=['GET'])
def course():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM course")
    coursedetails = cur.fetchall()
    return render_template('course.html', coursedetails=coursedetails)


@app.route('/department', methods=['GET'])
def department():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM department")
    departmentdetails = cur.fetchall()
    return render_template('department.html', departmentdetails=departmentdetails)


@app.route('/addcollege', methods=['GET', 'POST'])
def addcollege():
    form = CollegeForm()
    if form.validate_on_submit():
        code = form.code.data
        name = form.name.data
        number = form.number.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO college VALUES(%s, %s, %s)", (number, code, name))
        mysql.connection.commit()
        cur.close()
        flash('College added', 'success')
        return redirect(url_for('college'))
    return render_template('addcollege.html', form=form)


@app.route('/addcourse', methods=['GET', 'POST'])
def addcourse():
    form = CourseForm()
    if form.validate_on_submit():
        code = form.code.data
        name = form.name.data
        number = form.number.data
        college = form.myField.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO course VALUES(%s, %s, %s, %s)", (number, code, name, college))
        mysql.connection.commit()
        cur.close()
        flash('Course added', 'success')
        return redirect(url_for('course'))
    return render_template('addcourse.html', form=form)


@app.route('/adddepartment', methods=['GET', 'POST'])
def adddepartment():
    form = DepartmentForm()
    if form.validate_on_submit():
        number = form.number.data
        name = form.name.data
        college = form.myField.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO department VALUES(%s,%s,%s)", (number, name, college))
        mysql.connection.commit()
        cur.close()
        flash('Department added', 'success')
        return redirect(url_for('department'))
    return render_template('adddepartment.html', form=form)


@app.route('/addstudents', methods=['GET', 'POST'])
def addstudents():
    form = RegisterForm()
    if form.validate_on_submit():
        studentid = form.studentid.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        year = form.year.data
        course = form.field1.data
        department = form.field2.data
        college = form.field3.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students VALUES(%s, %s, %s, %s, %s, %s, %s)",
                    (studentid, firstname, lastname, year, course, department, college))
        mysql.connection.commit()
        cur.close()
        flash('Student added', 'success')
        return redirect(url_for('dashboard'))
    return render_template('addstudents.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = Searchform()
    if form.validate_on_submit():
        studentid = request.form['studentid']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM students WHERE studentid=%s", [studentid])
        if result > 0:
            student = cur.fetchone()
            return render_template('profile.html', student=student)
        else:
            flash('No Student found', 'danger')
        cur.close()
    return render_template('search.html', form=form)


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    form = RegisterForm()
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        studentid = request.form['studentid']
        year = form.year.data
        course = form.field1.data
        department = form.field2.data
        college = form.field3.data
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE students SET firstname=%s, lastname=%s, year=%s, course_code=%s, department_name=%s, college_code=%s "
            "WHERE studentid=%s", (firstname, lastname, year, course, department, college, studentid))
        flash("Data Updated Successfully", 'success')
        mysql.connection.commit()
        return render_template('dashboard.html')
    return render_template('edit.html', form=form)

@app.route('/editcollege', methods=['POST', 'GET'])
def editcollege():
    form = CollegeForm()
    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        number = request.form['number']
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE college SET code=%s, name=%s "
            "WHERE number=%s", (code,name, number))
        flash("Data Updated Successfully", 'success')
        mysql.connection.commit()
        return render_template('dashboard.html')
    return render_template('editcollege.html', form=form)

@app.route('/editdepartment', methods=['POST', 'GET'])
def editdepartment():
    form = DepartmentForm()
    if request.method == 'POST':
        college = request.form['myField']
        name = request.form['name']
        number = request.form['number']
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE department SET name=%s, college_code=%s "
            "WHERE number=%s", (name, college, number))
        flash("Data Updated Successfully", 'success')
        mysql.connection.commit()
        return render_template('dashboard.html')
    return render_template('editdepartment.html', form=form)

@app.route('/editcourse', methods=['GET', 'POST'])
def editcourse():
    form = CourseForm()
    if form.validate_on_submit():
        code = request.form['code']
        name = request.form['name']
        number = request.form['number']
        college = form.myField.data
        cur = mysql.connection.cursor()
        cur.execute("UPDATE course SET code=%s, name=%s, college_code=%s"
                    "WHERE number=%s", (code, name, college, number))
        mysql.connection.commit()
        cur.close()
        flash('Course added', 'success')
        return redirect(url_for('course'))
    return render_template('addcourse.html', form=form)


@app.route('/delete/<string:studentid>', methods=['GET'])
def delete(studentid):
    flash("Record Has Been Deleted Successfully", 'success')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE studentid=%s", (studentid,))
    mysql.connection.commit()
    return redirect(url_for('students'))


@app.route('/collegedelete/<string:code>', methods=['GET'])
def collegedelete(code):
    flash("College Has Been Deleted Successfully", 'success')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM college WHERE code=%s", (code,))
    mysql.connection.commit()
    return redirect(url_for('college')
                    )


@app.route('/departmentdelete/<string:name>', methods=['GET'])
def departmentdelete(name):
    flash("Department Has Been Deleted Successfully", 'success')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM department WHERE name=%s", (name))
    mysql.connection.commit()
    return redirect(url_for('department'))


@app.route('/coursedelete/<string:code>', methods=['GET'])
def coursedelete(code):
    flash("Course Has Been Deleted Successfully", 'success')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM course WHERE code=%s", (code,))
    mysql.connection.commit()
    return redirect(url_for('course'))


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret'
    app.run(debug=True)
