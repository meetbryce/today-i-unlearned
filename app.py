import datetime

from cs50 import SQL
from flask import Flask, render_template, request, flash, redirect, abort

app = Flask(__name__, static_url_path='/')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = SQL("sqlite:///tiu.db")


@app.errorhandler(404)
def not_found_handler(e):
    return render_template('404.html'), 404


@app.errorhandler(400)
def bad_request_handler(e):
    return render_template('400.html'), 400


@app.route('/', methods=["GET", "POST"])
def index_route():
    today = datetime.date.today()

    if request.method == "POST":
        try:
            year = int(request.form.get('year'))
        except ValueError:
            return abort(400)

        # check the user entered a year
        if not year:
            flash('Please enter the year you graduated')
            return render_template('index.html', max_year=today.year)

        # only accept years before this one! (might go further back depending on lesson quality)
        if year >= today.year:
            flash("Please enter a past year, we aren't in the business of making predictions!")
            return render_template('index.html', max_year=today.year)

        # don't accept years that are too far back
        if year < 1900:
            flash("Sorry, you can't go further back than 1900 right now.")
            return render_template('index.html', max_year=today.year)

        return redirect(f'/graduation-year/{year}')

    return render_template('index.html', max_year=today.year)


@app.route('/graduation-year/<year>', methods=["GET", "POST"])
def year_route(year: int):
    # check the year variable is an integer
    try:
        year = int(year)
    except ValueError:
        return abort(404)

    # reject any requests for future years
    today = datetime.date.today()
    if year >= today.year:
        flash("Please enter a past year, we aren't in the business of making predictions!")
        return abort(404)

    # don't accept years that are too far back
    if year < 1900:
        flash("Sorry, you can't go further back than 1900 right now.")
        return abort(404)

    # get all published lessons and calculate their usefulness based on any & all associated Votes
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
                           where published = true and start_year <= ?
                             and end_year >= ?)
        select id, title, content, sum(vote) + 37 as usefulness
        from lessons_and_votes
        group by 1, 2, 3
        order by usefulness desc
    ''', year, year)

    if not lessons:
        flash(f'We are still collecting lessons for the class of {year}. Come back soon.')

    # get the user's votes, so we can show votes that have already been cast
    ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    if not ip:
        ip = request.environ['REMOTE_ADDR']  # nb: in a test/local environment it will be 127.0.0.1

    # get and split all votes made with the current IP show we can show them in the UI
    votes_by_user = db.execute('select lesson_id, is_upvote from votes where user_ip = ?', ip)
    up_voted = [vote["lesson_id"] for vote in votes_by_user if vote["is_upvote"]]
    down_voted = [vote["lesson_id"] for vote in votes_by_user if not vote["is_upvote"]]

    return render_template('year.html', year=year, lessons=lessons, up_voted=up_voted, down_voted=down_voted)


@app.route('/vote/<year>/<lesson_id>', methods=["POST"])
def vote_route(year, lesson_id):
    # check we have a valid is_upvote
    try:
        is_upvote = bool(int(request.form.get('is_upvote')))
    except ValueError:
        return abort(400)

    ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    if not ip:
        ip = request.environ['REMOTE_ADDR']  # nb: in a test/local environment it will be 127.0.0.1

    # upsert the vote
    db.execute(
        'INSERT INTO votes (is_upvote, user_ip, lesson_id) VALUES (?, ?, ?) '
        'ON CONFLICT (user_ip, lesson_id) DO UPDATE SET is_upvote = ?',  # update existing if user already voted
        is_upvote, ip, lesson_id, is_upvote)

    flash(f'Thanks for your input! Your {"up" if is_upvote else "down"}vote was recorded.')

    return redirect(f'/graduation-year/{year}')


@app.route('/lesson/<lesson_id>', methods=["GET"])
def lesson_route(lesson_id: int):
    try:
        lesson = db.execute('select * from lessons where id = ? and published = true', lesson_id)[0]
    except IndexError:
        abort(404)
    return render_template('lesson.html', lesson=lesson)


@app.route('/lesson/<lesson_id>/feedback', methods=["GET", "POST"])
def lesson_feedback_route(lesson_id: int):
    if request.method == "POST":
        feedback = request.form.get('feedback')
        if not feedback:
            try:
                lesson = db.execute('select * from lessons where id = ? and published = true', lesson_id)[0]
            except IndexError:
                abort(404)
            return render_template('lesson_feedback.html', lesson=lesson, error=True)

        ip = request.environ.get('HTTP_X_FORWARDED_FOR')
        if not ip:
            ip = request.environ['REMOTE_ADDR']  # nb: in a test/local environment it will be 127.0.0.1

        db.execute('INSERT INTO feedback (lesson_id, user_ip, feedback) VALUES (?, ?, ?)', lesson_id, ip, feedback)

        return render_template('lesson_feedback_success.html')
    else:
        try:
            lesson = db.execute('select * from lessons where id = ? and published = true', lesson_id)[0]
        except IndexError:
            abort(404)
        return render_template('lesson_feedback.html', lesson=lesson)


@app.route('/suggest', methods=["GET", "POST"])
def suggest_route():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        start_year = request.form.get('start_year')
        end_year = request.form.get('end_year')

        if not (title and content and start_year and end_year):
            # todo: handle errors
            pass

        # end year should be after start year
        if not (end_year > start_year):
            # todo: handle error
            pass

        # create the lesson with published = false
        db.execute('insert into lessons (title, content, start_year, end_year, published) '
                   'values (?, ?, ?, ?, false)', title, content, start_year, end_year)

        return render_template('suggest_success.html', title=title, content=content,
                               start_year=start_year, end_year=end_year)
    return render_template('suggest.html')


if __name__ == '__main__':
    app.run()
