# Today I Unlearned

## Overview

### Video Demo

[//]: # (TODO: YouTube video URL here^^ )

### Description

[//]: # (TODO: write multi-paragraph description of the project)

## Code & Architecture

### Database Schema

* **feedback**: Feedback captures feedback provided by users about a given lesson, the IP address of the submitting user
  is recorded. Feedback is not surfaced in the UI but can be accessed directly in the database by an admin.
* **lessons**: Lessons are at the core of the Today I Unlearned product. A lesson represents something that was taught
  but later discovered to be incorrect. A lesson is associated with a period of time in which it would have been taught
  in schools. Lessons suggested by users through the platform are stored as unpublished lessons by
  setting `published=false`. Unpublished lessons are not surfaced in the UI but can be accessed directly in the database
  by an admin.
* **votes**: Votes are recorded on behalf of users when they press the upvote or downvote button (thumbs up / thumbs
  down). Whether a vote is an upvote or downvote is represented by the value of `is_upvote`. Each user (as determined by
  their IP address) can only have one vote on a given lesson. Changing votes from upvote to downvote is supported.

### `scripts/db-setup.sql`

This script contains all the SQL queries required to fully configure a blank SQLite DB.

This configures each of the key tables, links them via foreign key relationships, and adds appropriate indices.

This script should be run when creating a new database.

Usage: `sqlite3 tiu.db '.read ./scripts/db-setup.sql'`

### `src/styles.css`

This file is used to configure (i.e. import) Tailwind and adds the additional custom class I wanted for the flashing
messages.

### `static/script.js`

This script allows the user to dismiss the flashed message.

### `templates/400.html`

A custom error page for bad requests. Used when the user manages to get past the client-side validation and submits
invalid data in a POST request.

### `templates/404.html`

A custom error page for 404 Not Found errors. Used when an invalid URL is provided.

### `templates/index.html`

This is the homepage of the app. It provides an overview of what the site is about and provides a call to action for the
user to enter the year they graduated into the form.

The form is POSTed to the homepage URL and if it passes all validation checks, the user is redirected
to `/graduation-year/<year>`. If there are any issues, a helpful message is shown to the user using Flasks flashing
features.

### `templates/layout.html`

The layout used for the full app. It provides a block for 1) configuring the page `<title>`; and 2) injecting the page
content. Flashing message support is included too with the ability to dismiss the message. The overall layout is set to
make the footer sticky and have a non-sticky navbar. A "suggest a lesson" CTA is included in the footer on all pages
except the Suggest A Lesson page itself. The layout page handles the site wide CSS and JS.

### `templates/lesson.html`

This is the "share" page for a lesson. It serves as a permalink for each lesson and is surfaced to the user via the "
share" button on each lesson in the year view. The purpose of this page is to serve as a representation of the lesson to
Google and as a way for users to directly share an individual lesson with others.

### `templates/lesson_feedback.html`

This page allows the user to provide any feedback they have about a given lesson. The full lesson is shown on the page
so that the user can easily reference it when providing their feedback.

### `templates/lesson_feedback_success.html`

The success page shown to the user when they have successfully submitted feedback on an existing lesson. A back button
is shown which takes the user back 2 pages, which will be to wherever they were before visiting the feedback page.

### `templates/suggest.html`

This page allows the user to suggest a new lesson for the platform. This is a simple form that submits the data as
a `lesson` with `published=true` and ready for the admin to review the lesson and publish it manually if appropriate.

### `templates/suggest_success.html`

The success page shown to the user when they have successfully submitted a suggested lesson. Shows a "preview" of the
lesson to help give them a sense of immediate gratification since an admin needs to review the lesson before it is
manually published. A back button is shown which takes the user back 2 pages, which will be to wherever they were before
visiting the suggest a lesson page.

### `templates/year.html`

This shows a collection of lessons, this is used with the `/graduation-year/<year>` route to show all lessons relevant
to someone who graduated in that year. The lessons are ranked based on their Usefulness score (details below) to show
the most useful lessons first. Each lesson is presented with the ability to upvote, downvote, share, and provide
feedback.

### `tiu.db`

The application database. Included to help you easily get up and running.

### `tailwind.config.js`

I decided to use Tailwind as it's now a popular CSS framework. This file is used for its configuration. The setup is
quite basic, but I did add and install the 'forms' plugin.

### `app.py`

[//]: # (todo)

#### Usefulness Score

[//]: # (todo)

### `requirements.txt`

This outlines all the Python dependencies for my project and is used in the setup process by
running `pip install -r requirements.txt`

---

## Setup

1. `pip install -r requirements.txt`
2. If you don't have `tiu.db` (for example, if you want to start with a fresh database):
    * `touch tiu.db` to create the database
    * `sqlite3 tiu.db '.read ./scripts/db-setup.sql'` to setup the database tables, relations, and indices

## Development

1. Start the dev server `python -m flask run --port 8000 --debug`
2. Run the tailwind processor `npx tailwindcss -i ./src/styles.css -o ./static/styles.css --watch`

## Tasks

[//]: # (TODO: write full README - per the spec)

[//]: # (TODO: walkthru video - up to 3mins Your video should somehow include your project’s title, your name, 
          your city and country, and any other details that you’d like to convey to viewers.)

[//]: # (TODO: ensure the layout is fully responsive)

[//]: # (TODO: ensure no unhandled error cases)

[//]: # (TODO: check I've sufficiently commented the code... DOCSTRINGS!)

[//]: # (TODO: unit tests?)

[//]: # (TODO: Beam / Fathom analytics?)

[//]: # (TODO: dark mode?)

[//]: # (TODO: sitemap.xml ??)

[//]: # (TODO: make the aesthetic more education-y)

## Future ideas

- “similar lessons” using [SQLite cosine distance & embeddings](https://youtu.be/ArnMdc-ICCM?si=0wtGVZ8CEUOKKDLP) from
  Simon Willison
- leverage an LLM to generate additional content
- generate compelling OG Images to drive click-through rates
- extend the footer with links to popular years for SEO purposes