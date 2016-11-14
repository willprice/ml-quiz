#!/usr/bin/env bash
set -o errexit
PYTHON="${PYTHON:-python2}"
GIT="${GIT:-git}"

QUIZ="${1:-ml.quiz}"
QUIZ_HTML="${QUIZ%%.quiz}.html"
QUIZ_TARBALL="64496_15444.tar.gz"

"$GIT" checkout master
"$GIT" remote add deploy "git@github.com:willprice/ml-quiz.git"

[[ ! -f "$QUIZ" ]] && {
    echo "$QUIZ not found";
    exit 1;
}
echo yes | "$PYTHON" ./resources/compile_quiz.py --tarball "$QUIZ"
[[ -f "$QUIZ_TARBALL" ]] || {
    echo "Could not find generated tarball";
    exit 1;
}

"$PYTHON" ./resources/compile_quiz.py "$QUIZ"
[[ -f "$QUIZ_HTML" ]] || {
    echo "Could not find generated html";
    exit 1;
}
mv "$QUIZ_HTML" index.html

"$GIT" add .
"$GIT" commit -m "Generate quiz ($(date))"
"$GIT" push --force --quiet deploy master:gh-pages
