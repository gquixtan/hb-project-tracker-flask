"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def show_all():
    """ Show live links to all students and all projects """

    QUERY = """
    SELECT first_name, last_name, github
    FROM students
    """

    db_cursor = db.session.execute(QUERY)

    rows = db_cursor.fetchall()

    return rows



@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    # a list of (project_title, grade) for a given student
    titles_grades = hackbright.get_grades_by_github(github)


    html = render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github,
                            titles_grades=titles_grades)

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    html = render_template("student_search.html")

    return html


@app.route("/student-add")
def student_add():
    """ Show form for adding a student """

    html = render_template("student_add.html")

    return html

@app.route("/student-added", methods=['POST'])
def added_student():
    """ Collect data from form and add student to DB """

    first = request.form.get('first_name')
    last = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first, last, github)
    first, last, github = hackbright.get_student_by_github(github)

    html = render_template("student_added.html", first=first, last=last, github=github)

    return html

@app.route("/project")
def show_project():
    """ show the project title & description given a project title
    (from GET request)
    """

    title = request.args.get('title')

    title, description, grade = hackbright.get_project_by_title(title)

    grade_list = hackbright.get_grades_by_title(title)

    html = render_template("project.html", title=title,
                            description=description, grade=grade,
                            grade_list=grade_list)

    return html


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
