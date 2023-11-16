from flask import Flask, render_template, request, flash, redirect

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=["GET", "POST"])
def index_route():
    if request.method == "POST":
        year = int(request.form.get('year'))
        # check the user entered a year
        if not year:
            flash('Please enter the year you graduated')
            return render_template('index.html')

        # todo: check the user entered an acceptable valid year
        # todo: retrieve lessons from the db

        flash(f'Generating lessons for the class of {year}. Come back soon.')
        return redirect(f'/graduation-year/{year}')

    return render_template('index.html')


@app.route('/graduation-year/<year>', methods=["GET", "POST"])
def year_route(year):
    lessons = [
        {
            "id": 123,
            "content": "hello world. lorem ipsum...."
        },
        {
            "id": 456,
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla blandit enim nec urna "
                       "imperdiet efficitur. Proin eget purus turpis. Curabitur gravida malesuada urna, vel porttitor "
                       "dui rhoncus sit amet. Donec ac magna neque. Quisque vel nunc ante. Nam blandit lorem et "
                       "libero tempor auctor. Quisque ut libero vitae dui molestie lacinia vel quis ligula."
        }

    ]
    return render_template('year.html', year=year, lessons=lessons)


if __name__ == '__main__':
    app.run()
