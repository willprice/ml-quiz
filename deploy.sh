#!/usr/bin/env bash
PYTHON="${PYTHON:-python2}"
GIT="${GIT:-git}"

QUIZ="${1:-ml.quiz}"
QUIZ_TEMP="$(mktemp)"
QUIZ_HTML="${QUIZ%%.quiz}.html"

"$GIT" checkout master
"$PYTHON" ./resources/compile_quiz.py "$QUIZ"
mv "${QUIZ_HTML}" "${QUIZ_TEMP}"
"$GIT" checkout gh-pages
mv "${QUIZ_TEMP}" index.html
"$GIT" add index.html
"$GIT" commit -m "Generate quiz ($(date))"
"$GIT" push -u origin gh-pages
"$GIT" checkout -
