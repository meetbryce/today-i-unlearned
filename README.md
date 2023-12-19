# Today I Unlearned

## Overview

### Video Demo

[//]: # (TODO: YouTube video URL here^^ )

### Description

Today I Unlearned is a site intended to help solve the problem of things being taught in school later turning out to be
incorrect. It provides a place for people to unlearn things that were taught incorrectly based on the year they finished
school.

This idea was inspired by the many, many threads on Reddit asking people to list things they learned in school that they
have since learned to be false. These posts have been incredibly popular indicating that people might value a site like
Today I Unlearned (examples listed below). I've also seen a number of memes calling for a site like this e.g. "Website
idea: you input the year you graduated from high school and the website generates a list of outdated "facts" and
concepts you were taught in school that have since been disproven" based on
a [tweet](https://twitter.com/ericnakagawa/status/1335833653738258434) from 2020 with 20k likes!

Today I Unlearned provides a place not only to unlearn, but also to upvote/downvote lessons based on your own
experience, provide feedback on existing lessons, and even suggest your own lessons too!

Some of the many Reddit threads trying to meet this need:

* ["What’s a fact that was taught in school that’s been disproven in your lifetime?"](https://www.reddit.com/r/AskReddit/comments/1789w9u/whats_a_fact_that_was_taught_in_school_thats_been/),
  Oct 2023, 11.8k comments, 12.6k karma
* ["What were the 'facts' you learned in school, that are no longer true?"](https://www.reddit.com/r/AskReddit/comments/69dex7/what_were_the_facts_you_learned_in_school_that/),
  May 2017, 30.6k comments, 30.7k karma
* ["What was a fact taught to you in school that has been disproven in your lifetime?"](https://www.reddit.com/r/AskReddit/comments/6wiqew/what_was_a_fact_taught_to_you_in_school_that_has/),
  Aug 2017, 25.3k comments, 29.5k karma
* ["What did you learn in Elementary school that turned out to be false/ a lie when you reached adulthood?"](https://www.reddit.com/r/AskReddit/comments/sy3qke/what_did_you_learn_in_elementary_school_that/),
  Feb 2022, 14.2k comments, 27.5k karma
* ["What did you learn in school that turned out to be absolutely useless?"](https://www.reddit.com/r/AskReddit/comments/m0nvnq/what_did_you_learn_in_school_that_turned_out_to/),
  Mar 2021, 315 comments, 74 karma
* ["What's something you learned in school that was false?"](https://www.reddit.com/r/AskReddit/comments/2feflc/whats_something_you_learned_in_school_that_was/),
  Sep 2014, 547 comments, 139 karma
* ["What was the most harmful thing you were taught in school?"](https://www.reddit.com/r/AskReddit/comments/3pwj65/what_was_the_most_harmful_thing_you_were_taught/),
  Oct 2015, 1.1k comments, 500 karma

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
so that the user can easily reference it when providing their feedback. The title of the lesson is included to maintain
continuity in context while the user writes their feedback.

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

This is the core of the application backend.

* `not_found_handler()` allows us to use our custom 404 error page anytime a 404 error occurs
* `bad_request_handler()` allows us to use our custom 400 error page anytime a 400 error occurs
* `index_route()` renders the index template and processes the post request from any "enter the year you graduated"
  forms. It checks the year provided is valid (mostly as a backup to the client-side validation of the same rules) and
  provides helpful error messages using the flashing system.
* `year_route()` renders the year template. Checks the year is valid (mostly as a backup to the client-side validation
  of the same rules) and throws a 404 error if it is invalid. For a valid year, we fetch the lessons joined with votes
  to calculate the Usefulness Score (details below). If there are no lessons found, we render a message using the
  flashing system. We then get the user's IP address (with a fallback for local/dev contexts). We then use the IP
  address to get all votes cast with that IP address (used to indicate in the UI whether a vote has been cast). To avoid
  extra SQL requests (which may be slow), we pull all votes and then filter them into upvotes and downvotes in python.
* `vote_route()` accepts votes from the frontend with safety checks that throw a 400 error if they don't succeed. As
  above, we get the user IP with a fallback method for local development. We then upsert the vote into the database and
  render a flashed message
* `lesson_route()` checks that a lesson with the provided ID exists and is published. If so, it's rendered. Otherwise, a
  404 error is thrown.
* `lesson_feedback_route()` renders the feedback form when the URL is loaded normally, also captures and processes the
  form data when POSTed to. Checks the form data is valid (providing flashed messages if the data is invalid), gets the
  user IP and stores both in the database in the `feedback` table before rendering the success page to the user.
* `suggest_route()` renders the suggest a lesson form when the URL is loaded normally, also captures and processes the
  form data when POSTed to. Checks the form data is valid (providing flashed messages if the data is invalid) and then
  stores it in the database in the `lessons` table (with `published=false` so it isn't shown to users without being
  reviewed by an admin) before rendering the success page to the user.

#### Usefulness Score

The usefulness score is based on a simple algorithm to help provide a vote-informed score that's also intuitive, even
without many (or even any) votes. As the site scales and sees more votes, it may make sense to improve the algorithm,
but this should work for a long while. The method is to take a base usefulness score of 37, add 1 for each upvote, and
subtract 1 for each downvote.

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

[//]: # (TODO: walkthru video - up to 3mins Your video should somehow include your project’s title, your name, 
          your city and country, and any other details that you’d like to convey to viewers.)

[//]: # (TODO: ensure the layout is fully responsive)

## Future ideas

- make the aesthetic even more education-y => https://arc.net/folder/2B6B7588-BF29-476E-B839-DB4842C2C93C
- dark mode
- generate sitemap.xml for SEO purposes => https://github.com/h-janes/flask-sitemapper/wiki/Usage#recommended-method
- explicitly define OG meta tags (etc.) so links always look great on social media
- add Fathom or Beam Analytics to keep track of actual user behavior
- “similar lessons” via Scott Willison's SQLite cosine distance &
  embeddings [link](https://youtu.be/ArnMdc-ICCM?si=0wtGVZ8CEUOKKDLP)
- leverage an LLM to generate additional content
- generate compelling OG Images to drive click-through rates
- extend the footer with links to popular years for SEO purposes
- generate illustrations using stable diffusion to help make the site more visually engaging
