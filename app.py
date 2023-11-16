import datetime

from cs50 import SQL
from flask import Flask, render_template, request, flash, redirect

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQL("sqlite:///tiu.db")


@app.route('/', methods=["GET", "POST"])
def index_route():
    if request.method == "POST":
        year = int(request.form.get('year'))
        # check the user entered a year
        if not year:
            flash('Please enter the year you graduated')
            return render_template('index.html')

        # only accept years before this one! (might go further back depending on lesson quality)
        today = datetime.date.today()
        if year >= today.year:
            flash("Please put a past year, we aren't in the business of making predictions!")
            return render_template('index.html')

        # todo: check the year isn't too far back!

        return redirect(f'/graduation-year/{year}')

    return render_template('index.html')


@app.route('/graduation-year/<year>', methods=["GET", "POST"])
def year_route(year):
    # todo: check the route is legit

    lessons = db.execute('select id, content from lessons where year = ?', year)

    if not lessons:
        flash(f'Generating lessons for the class of {year}. Come back soon.')

    return render_template('year.html', year=year, lessons=lessons)


if __name__ == '__main__':
    app.run()
