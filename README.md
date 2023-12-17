# Today I Unlearned
### Video Demo:  <URL HERE>
## Description:
[//]: # (TODO)
### Code & Architecture
[//]: # (todo: what each of the files you wrote for the project contains and does, & if you debated certain design 
          choices, explaining why you made them.)
#### scripts/db-setup.sql
#### src/styles.css
#### templates/400.html
#### templates/404.html
#### templates/index.html
#### templates/layout.html
#### templates/lesson.html
#### templates/lesson_feedback.html
#### templates/lesson_feedback_success.html
#### templates/suggest.html
#### templates/suggest_success.html
#### templates/year.html
#### tiu.db
#### tailwind.config.js
#### app.py
#### requirements.txt

## Setup

1. `pip install -r requirements.txt`

## Development

1. Start the dev server `python -m flask run --port 8000 --debug`
2. Run the tailwind processor `npx tailwindcss -i ./src/styles.css -o ./static/styles.css --watch`

## Tasks
[//]: # (TODO: ensure the layout is fully responsive)
[//]: # (TODO: ensure no unhandled error cases)
[//]: # (TODO: check I've sufficiently commented the code)
[//]: # (TODO: double check I've fully met the requirements in the spec)
[//]: # (TODO: unit tests?)
[//]: # (TODO: analytics?)
[//]: # (TODO: dark mode?)
[//]: # (TODO: sitemap.xml ??)

## Future ideas

- “similar lessons” using [SQLite cosine distance & embeddings](https://youtu.be/ArnMdc-ICCM?si=0wtGVZ8CEUOKKDLP) from
  Simon Willison
- leverage an LLM to generate additional content
- generate compelling OG Images to drive click-through rates

[//]: # (TODO: write full README - per the spec)
[//]: # (TODO: walkthru video - up to 3mins Your video should somehow include your project’s title, your name, 
          your city and country, and any other details that you’d like to convey to viewers.)
