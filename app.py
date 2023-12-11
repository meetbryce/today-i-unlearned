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

    lessons = db.execute('''
        with lessons_and_votes as (select l.id,
                                  title,
                                  content,
                                  case
                                      when is_upvote = TRUE then 1
                                      when is_upvote = FALSE then -1
                                      else 0
                                      end as vote
                           from lessons l
                                    left join main.votes v on l.id = v.lesson_id
                           where start_year <= ?
                             and end_year >= ?)
        select id, title, content, sum(vote) + 37 as usefulness
        from lessons_and_votes
        group by 1, 2, 3
        order by usefulness desc
    ''', year, year)

    if not lessons:
        flash(f'We are still collecting lessons for the class of {year}. Come back soon.')

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


@app.route('/lesson/<lesson_id>', methods=["GET"])
def lesson_route(lesson_id):
    if not lesson_id:
        # todo: error
        pass

    lesson = db.execute('select * from lessons where id = ?', lesson_id)[0]
    return render_template('lesson.html', lesson=lesson)


@app.route('/lesson/<lesson_id>/feedback', methods=["GET", "POST"])
def lesson_feedback_route(lesson_id):
    if not lesson_id:
        # todo: error
        pass
        #  or
    if request.method == "POST":
        # todo: capture the feedback
        pass
    else:
        lesson = db.execute('select * from lessons where id = ?', lesson_id)[0]
        return render_template('lesson_feedback.html', lesson=lesson)


if __name__ == '__main__':
    app.run()
