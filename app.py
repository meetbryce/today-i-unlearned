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
    # todo: check the year variable is legit

    lessons = db.execute(
        'select id, title, content from lessons where start_year <= ? and end_year >= ?', year, year)
    # todo: order by usefulness

    if not lessons:
        flash(f'Generating lessons for the class of {year}. Come back soon.')

    # todo: indicate when vote already cast

    return render_template('year.html', year=year, lessons=lessons)


@app.route('/vote/<year>/<lesson_id>', methods=["POST"])
def vote_route(year, lesson_id):
    is_upvote = bool(int(request.form.get('is_upvote')))

    ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    if not ip:
        ip = request.environ['REMOTE_ADDR']  # nb: in a test/local environment it will be 127.0.0.1

    db.execute(
        'INSERT INTO votes (is_upvote, user_ip, lesson_id) VALUES (?, ?, ?) '
        'ON CONFLICT (user_ip, lesson_id) DO UPDATE SET is_upvote = ?',  # update existing if user already voted
        is_upvote, ip, lesson_id, is_upvote)

    flash(f'Thanks for your input! Your {"up" if is_upvote else "down"}vote was recorded.')

    return redirect(f'/graduation-year/{year}')


if __name__ == '__main__':
    app.run()
