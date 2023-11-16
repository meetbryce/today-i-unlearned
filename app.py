from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index_route():  # put application's code here
    return render_template('index.html')


@app.route('/<year>', methods=["GET", "POST"])
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
