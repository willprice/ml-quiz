#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"
REPO=$(cat $DIR/../.git/config | grep "url = .*\.git" | sed -e "s/.*url = .*\/\(.*\)\.git.*/\1/")

# if quiz filename not given use default
if [ $1 ]
then
  echo "Deploying $1 to gh-pages"
  QUIZ="$1"
else
  echo "Quiz file to deploy not given; using my_quiz.quiz"
  QUIZ="$DIR/../my_quiz.quiz"
fi

if [ "$REPO" =  "quick-quiz" ]
then
  git checkout gh-pages
  git merge master
  $DIR/compile_quiz.py "$QUIZ"
  git commit -m "deploy to pages $(date)"
  git push origin gh-pages
  git checkout master
else
  echo "Could not locate 'quick-quiz' git repository; please deploy to gh-pages manually"
fi
