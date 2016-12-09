#!/usr/bin/env bash
set -o errexit
PYTHON="${PYTHON:-python2}"
GIT="${GIT:-git}"

QUIZ="${1:-ml.yaml}"

"$GIT" checkout master
"$GIT" remote add deploy "git@github.com:willprice/ml-quiz.git"

[[ ! -f "$QUIZ" ]] && {
    echo "$QUIZ not found";
    exit 1;
}

echo yes | ./compile.sh "$QUIZ"

"$GIT" add --force "${QUIZ%%.yaml}"*.html
"$GIT" commit -m "Generate quiz ($(date))"
"$GIT" push --force --quiet deploy master:gh-pages
