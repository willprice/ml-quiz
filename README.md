# Quick quiz generator
A quick quiz generator focused on content and not platform.

Each quiz file must contain definitions of:
 - `uid:` - your Bristol user ID,
 - `title:` - the title of your quiz,
 - `url:` - url to your quiz if you host it on GitHub and have published it on GitHub Pages.

Comments are introduced with `//`.

Each question is wrapped in between `#1` and `1#`, where `1` in this example is question number. Numbers given to the questions don't have to be in order but the questions will be sorted based on the number before displaying.

## Types of question ##
You can specify the following types of question:
 - Single choice (`single` keyword)
 - Multiple choice (`multi` keyword)
 - Order elements (`order` keyword)
 - Fill in blanks (`blanks` keyword)

You define the type of question in `answer:` flag - see below for details.  
See the example attached below for usage.

## Types of answers ##
Each type of question needs properly formated answers.  
For *single choice* questions the answer is defined by a bullet list with `-` marking incorrect answer and `*` indicating the correct one, e.g.:
```
 - False
 - Another False
 * True
 - One more false
```
For the *miltiple choice* follow the same strategy but with multiple `*` indicators, e.g.:
```
 - False
 * True
 - Another False
 * One More True
```
For *ordering questions* please specify the correct order with `1)`, `2)`, etc., e.g.:
```
 2) This is the second element
 4) This is the fourth element
 1) This is the first element
 3) This is the third element
```
Finally, for the *filling-in blanks* questions please do not provide any kind of answer in the `answer:blanks:` tag. Instead alter the `quiestion:` tag by putting words to be asked in square brackets, e.g. `this [word] will be asked`.

For more details please see attached below `.quiz` file.

## Required parameters ##
The following parameters are required:
 - `difficulty:` defines difficulty of the questions; possibilities are: *easy*, *medium* and *hard*
 - `reference:` defines ML book chapter and section that the question corresponds to; it is given in format **chapter.section** e.g. `5.12`
 - `question:` defines the question that will be asked; it must be contained in one line; both *in-line* LaTeX (i.e. `$\LaTeX`) and *display* LaTeX (i.e. `$$\LaTeX$$`) are supported.
 - `answers:_question type_:_question answers_` defines type and possible answers to the question; see above for details.

## Optional parameters ##
You can optionally attach image to your question with (caption is not required):
 - `image:My caption:path/to/my/image.jpg` or
 - `image::path/to/my/image.jpg`

Another optional parameter is *response text*. If specified it will appear upon question attempt (`response:` keyword):
 - `response: This text appears upon question attempt`

## Restrictions ##
The `.quiz` files are compiled to JSON with use of *regular expressions*. This means that if any of your question does not follow the syntax rules it will be omitted.  
The main restriction at the moment is that each parameter must be defined in **one line only**. Please see example below for details.

## Online quiz example ##
See an [example quiz](http://so-cool.github.io/quick-quiz/).

# Usage #

First, create a quiz text file using the following format (named `my_quiz.quiz` for example)

```
// example quiz text
// <- (this is a comment and will be ignored)

// this is the url for your quiz
url: http://so-cool.github.io/quick-quiz/

// this is your UoB username
uid: ab12345

// this is the title of the quiz
title: Quizk-quiz show-off.

// this is an example question.
// the number signifies the question order,
// meaning questions can be placed in random order
// within the file
#1
difficulty : easy
reference : 5.15
question: 
  Which of the following is $\LaTeX$ equation?
image::img/img1.jpg
image: my caption : img/img2.jpg

  // these are answers, a correct answer
  // is indicated by a "*"
answers:single:
  - 2 + 2
  - 2 + 3
  * $ \frac{7}{2} + 3 $
  - seven plus two

  // this is a reponse text paragraph
  // it will be displayed upon answering the question
response:
  You know $\LaTeX$! That's great!
1#

#2
difficulty : medium
reference : 2.2
question :
  Mark all the letters:
answers:multi:
  * T
  * F
  - 7
  * w
2#

#3
difficulty : hard
reference : 12.2
question:
  Order the following numbers:
answers:order:
  2) 26
  1) 19
  3) 100
3#

#4
difficulty: hard
reference: 3.4
question:
  $2+2$ is {4}. What colour is red truck: {red}.
answers:blanks:
4#
```

Then, parse it into a json file and create corresponding `index.html` file using `quiz_questions.py my_quiz.quiz`...
```shell
python quiz_questions.py my_quiz.quiz
```

This produces a formatted json file like this...
```javascript
{
  "questions": [
    {
      "answer_type": "single",
      "answers": [
        "2 + 2",
        "2 + 3",
        "$ \\frac{7}{2} + 3 $",
        "seven plus two"
      ],
      "captions": [
        "",
        "my caption"
      ],
      "chapter": 5,
      "correct": [
        2
      ],
      "difficulty": "easy",
      "images": [
        "img/img1.jpg",
        "img/img2.jpg"
      ],
      "number": 1,
      "prompt": "Which of the following is $\\LaTeX$ equation?",
      "section": 15,
      "text": "You know $\\LaTeX$! That's great!"
    },
    {
      "answer_type": "multi",
      "answers": [
        "T",
        "F",
        "7",
        "w"
      ],
      "chapter": 2,
      "correct": [
        0,
        1,
        3
      ],
      "difficulty": "medium",
      "number": 2,
      "prompt": "Mark all the letters:",
      "section": 2
    },
    {
      "answer_type": "order",
      "answers": [
        "26",
        "19",
        "100"
      ],
      "chapter": 12,
      "correct": [
        2,
        1,
        3
      ],
      "difficulty": "hard",
      "number": 3,
      "prompt": "Order the following numbers:",
      "section": 2
    },
    {
      "answer_type": "blanks",
      "chapter": 3,
      "correct": [
        "4",
        "red"
      ],
      "difficulty": "hard",
      "number": 4,
      "prompt": [
        "$2+2$ is ",
        0,
        ". What colour is red truck: ",
        1,
        "."
      ],
      "section": 4
    }
  ],
  "title": "Quizk-quiz show-off.",
  "uid": "ab12345",
  "url": "http://so-cool.github.io/quick-quiz/"
}
```

and `index.html` like this:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
  <title>My Quiz</title>
  <link href="http://fonts.googleapis.com/css?family=Lato:300,400" rel="stylesheet" type="text/css">
  <link rel="stylesheet" href="resources/css/bootstrap.min.css">
  <link rel="stylesheet" type="text/css" href="resources/css/sweet-alert.css">
  <link rel="stylesheet" href="resources/css/quiz.css">
  <style>
    #quiz {
      height: 600px;
      display: block;
    }
  </style>
  <script type="text/x-mathjax-config">
     MathJax.Hub.Config({
       tex2jax: {
         inlineMath: [ ['$','$'] ],
         displayMath: [ ['$$','$$'] ]
       }
     });
  </script>
  <script
     type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
</head>
<body>
  <div class="container-fluid">
    <div id="quiz"></div>
  </div>
  <script src="resources/js/jquery-1.11.3.min.js"></script>
  <script src="resources/js/bootstrap.min.js"></script>
  <script src="resources/js/sweet-alert.min.js"></script>
  <script src="resources/js/quiz.js"></script>
  <script type='text/javascript' src='http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'></script>
  <script>
    $(function() {
      $('#quiz').quiz("my_quiz.json");
    });
  </script>
</body>
</html>
```

Now merge *master* branch of your repository with *gh-pages* branch and push it to GitHub (you can do this with `deploy_ghpages.sh` script e.g. `deploy_ghpages.sh my_quiz.quiz`). Congratulations, your quiz is now online accessible at `your-github-username.github.io/quick-quiz`.

# Quiz development #
For developing the quiz at your machine please use `serve_quiz.py` script, e.g. `serve_quiz.py my_quiz.quiz`. It checks `my_quiz.quiz` file every 5 seconds for changes and rebuilds JSON file if necessary.  
It also publishes your quiz at `127.0.0.1:8888` by default so you can preview your work.

# TODO #
 - [ ] Insert image in response text.
 - [ ] Multi-line questions.
 - [ ] Add question type: *match*
