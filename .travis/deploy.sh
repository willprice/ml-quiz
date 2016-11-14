#!/usr/bin/env bash
PYTHON="${PYTHON:-python2}"
GIT="${GIT:-git}"

QUIZ="${1:-ml.quiz}"
QUIZ_HTML="${QUIZ%%.quiz}.html"
QUIZ_TEMP="$(mktemp)"

"$GIT" checkout master

[[ ! -f "$QUIZ" ]] && {
    echo "$QUIZ not found";
    exit 1;
}

"$PYTHON" ./resources/compile_quiz.py "$QUIZ"
[[ ! -f "$QUIZ_HTML" ]] && exit 1;
mv "${QUIZ_HTML}" "${QUIZ_TEMP}"

"$GIT" fetch --all
"$GIT" checkout --orphan gh-pages
mv "${QUIZ_TEMP}" index.html
"$GIT" status index.html | grep 'modified' 2>&1 > /dev/null
if [[ $? -ne 0 ]]; then
    echo "No changes to push, exiting"
    exit 0;
fi
"$GIT" add index.html
"$GIT" commit -m "Generate quiz ($(date))"
"$GIT" push -u origin gh-pages