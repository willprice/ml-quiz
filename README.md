# Quick quiz generator
A quick quiz generator focused on content; not platform.

To generate a quiz create a text file with `.quiz` extension in the root of this folder structure (where `README.md` is located).

Each quiz file must contain definition of:

 - `uid:` - your Bristol user ID e.g. `uid:ab12345` (if more than one person is working on a quiz please insert one `uid:` entry per person),
 - `title:` - the title of your quiz e.g. `title: My awesome ML quiz`,
 - `url:` - url to your quiz; if you host it on GitHub give a link to your GitHub repository otherwise put `url: 127.0.0.1`.

Comments in the quiz file are introduced with `//`.

Each question is wrapped between `#1` and `1#`, where `1` in this example is question number. Numbers given to the questions don't have to be in order; they will be randomised before displaying.

## Types of question ##
You can specify the following types of question:

 - Single choice (`single` keyword)
 - Multiple choice (`multiple` keyword)
 - Order elements (`sort` keyword)
 - Fill in blanks (`blank_answer` keyword)
 - Fill in contingency matrix (`cloze_answer` keyword)
 - Match objects (`matrix_sort_answer` keyword)

You define the type of question in `answer:` flag e.g. `answer:single:` - see the example attached below for details.

### Specifying answer for each type of question ###
Each type of question needs properly formated answers.  
For *single choice* questions the answer is defined by a bullet list with `-` marking incorrect answer and `*` indicating the correct one, e.g.:
```
answer:single:
 - False
 - Another False
 * True
 - One more false
```
For the *miltiple choice* follow the same strategy but with multiple `*` indicators, e.g.:
```
answers:multiple:
 - False
 * True
 - Another False
 * One More True
```
For *ordering questions* please specify the correct order with `1)`, `2)`, etc., e.g.:
```
answers:sort:
 2) This is the second element
 4) This is the fourth element
 1) This is the first element
 3) This is the third element
```
For the *filling-in blanks* questions please do not provide any kind of answer in the `answer:blank_answer:` tag. Instead alter the `quiestion:` tag by putting words to be asked in square brackets, e.g.
```
question:
  This [word] will be asked.

answers:blank_answer:
```
If more than one answer is correct please separate them by comma inside the square brackets e.g. `[blue,yellow,green]`.  
For *filling-in contingency matrix* in the answer field create text based matrix e.g.
```
answers:cloze_answer:

1 | 4 | 5
----------
2 | 5 | 7
----------
3 | 9 | 12

```
Where the numbers are as follows:

|          | Predicted + | Predicted - |    |
|----------|-------------|-------------|----|
| Actual + | 1           | 4           | 5  |
| Actual - | 2           | 5           | 7  |
|          | 3           | 9           | 12 |

Finally, for *object matching* create bullet list containing question and answer separated by `<->` symbol i.e. `- question <-> answer` e.g.
```
answers:matrix_sort_answer:
  - The letter after 'a' is <-> B.
  - The letter after 'g' is <-> H.
  - I like                  <-> alphabet.
```

For more details please see `.quiz` file attached below.

## Question flags ##
### Required parameters ###
The following parameters are required:

 - `difficulty:` defines difficulty of the questions; possibilities are: *easy*, *medium* and *hard*.
 - `reference:` defines ML book chapter and section that the question corresponds to; it is given in format **chapter<dot>section** e.g. `5.12`.
 - `question:` defines the question text that will be asked; it must be contained in one line; both *in-line* LaTeX (i.e. `$\LaTeX$`) and *display* LaTeX (i.e. `$$\LaTeX$$`) are supported.
 - `answers:_question type_:_question answers_` defines type and possible answers to the question; see above for details.

### Optional parameters ###
You can optionally attach image(s) to your question with:
```
image:My caption:
  path/to/my/image.jpg
```
or
```
image::
  path/to/my/image.jpg
```
caption is not required.

## Restrictions ##
The `.quiz` files are compiled to (JSON) HTML with use of *regular expressions*. This means that if any of your question does not follow the syntax rules it will be omitted. Unfortunately regex matcher cannot produce any error messages therefore the question simply won't be outputted without any message.

To make sure that your questions get compiled please follow the example given below as close as possible. The major restriction of the compiler at the moment is that each parameter must be defined in **one line only**. Please see example below for details.

Moreover, the following order of question tags **must** be preserved:

 - `difficulty`
 - `reference`
 - `question`
 - `image::` (optional)
 - `answers::`

Finally, your quiz file must have `.quiz` extension and need to be placed in root folder of this repository.

It requires `Python 2.x` and works on Linux (2.11MVB machines) and Unix (OS X).

## Syntax ##
As the quiz file is translated into HTML the questions and answers support HTML tags e.g. `<br>` for new line.

Moreover, both *in-line* LaTeX (introduced by `$` environment e.g. `$\LaTeX$`) and *display* LaTeX (introduced by `$$` environment e.g. `$$\LaTeX$$`) are supported.

## Online quiz example ##
See an [example quiz](http://so-cool.github.io/quick-quiz/my_quiz.html).

## Not compiling questions ##
If your question is not compiling and you have followed all the rules given in this document you can email me for help.  
The recommended approach to developing your questions is one question per file during their creation and combining the into one file before submission.

# Usage #
## Create `.quiz` file ##
First, create a quiz text file using the following format (named `my_quiz.quiz` for example):

```
// example quiz text
// <- (this is a comment and will be ignored)

// this is the url for your quiz
url: http://so-cool.github.io/quick-quiz/

// this is your UoB username
uid: ab12345
// uncomment the next line if you're working in a pair
// uid: cd67890

// this is the title of the quiz
title: Quizk-quiz show-off.

// this is an example question.
// the number signifies the question order,
// meaning questions can be placed in random order
// within the file
#1
difficulty : easy
reference : 5.2
question:
  Which of the following is $\LaTeX$ equation?
image::
  img/unicorn.jpg
image: my caption :
  img/unicorn.jpg
// these are answers, a correct answer
// is indicated by a "*"
answers:single:
  - 2 * 2
  - 2 - 3
  * $ \frac{7}{2} + 3 $
  - seven plus two
1#

#2
difficulty : medium
reference : 2.2
question :
  Mark all the letters:
answers:multiple:
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
answers:sort:
  2) 26
  1) 19
  3) 100
3#

#4
difficulty: hard
reference: 3.3
question:
  $2+2$ is [4]. What colour is a red truck: [red,Red].
answers:blank_answer:
4#

#5
difficulty: hard
reference: 3.3
question:
  Fill in contingency matrix.<br><br>1TP<br>5TN<br>12 in total<br>5 actual positive
answers:cloze_answer:

1 | 4 | 5
----------
2 | 5 | 7
----------
3 | 9 | 12

5#

#6
difficulty: hard
reference: 3.3
question:
  Match the following sentences.
answers:matrix_sort_answer:
  - The letter after 'a' is <-> B.
  - The letter after 'g' is <-> H.
  - I like <-> alphabet.
6#

```

## Compiler usage ##
Then, parse it into an HTML file using `quiz_questions.py my_quiz.quiz`...
```shell
python ./resources/compile_quiz.py ./my_quiz.quiz
```

And open resulting `./my_quiz.html` in your web browser.

### Compiler options ###
To see the compiler options do `./resources/compile_quiz.py -h`. The options are:
```bash
optional arguments:
  -h, --help            show this help message and exit
  -q QUESTION, --question QUESTION
                        the # of question to be generated (all questions are
                        generated by default)
  -a, --all             generate all of the questions
  -s, --separate        generate all of the questions in separate files
  -i, --iframe          generate all of the question on one page (iframe)
  -o, --order           order the questions first on book section then on
                        difficulty
  -O, --Order           order the questions first on difficulty then on book
                        section
  -d, --debug           indicate the correct answer in the question
  -f, --feedback        generate feedback for all questions
  -e, --extract         export marked questions to separate file
  -c, --count           show difficulty statistics of the quiz file
  -t, --tarball         tarball the quiz for submissions
```

Therefore, flag `-a` compiles all of the questions in given `.quiz` file into one HTML. `-q 7` compiles only question `#7`. `-s` will compile all of the questions and place each one in separate HTML file. `-i` generates `iframe` based HTML displaying all questions on one page.  
`-d` will generate an HTML with correct answers indicated by *chevron* symbol - really useful feature for questions development. `-c` will produce question difficulty statistics. And `-o`/`-O` will create additional `.quiz` file with questions sorted as described above.  
Finally, `-t` creates a *tarball* (archive) with all files necessary for submission.

# Submission #
Please submit only the following files:

- A tarball with your quiz created with `-t` option.
- A short report (2-4 pages) in `pdf` format describing for each question briefly what knowledge it tests, and what your rationale for classifying it as easy/medium/hard is. Your submission will primarily be marked on the diversity and originality of your questions, as well as your assessment of their difficulty level.
    * An easy question is one that can be answered by looking up a specific passage in the book;
    * a medium question is one that requires some degree of problem-solving;
    * a hard question is one that requires some thinking beyond what was discussed in the lectures.

# Assignment description #
Full assignment description is available [here](https://github.com/So-Cool/quick-quiz/wiki/Option-3:-ML-Quiz).

# Marking - markers only #
**Please do not use these options!**

## Feedback ##
For marking purposes you may leave feedback to each question with additional flag `feedback` e.g.:
```
#1
feedback:
  It is too easy.
difficulty : easy
reference : 5.2
question:
  Which of the following is $\LaTeX$ equation?
image::
  img/unicorn.jpg
image: my caption :
  img/unicorn.jpg
// these are answers, a correct answer
// is indicated by a "*"
answers:single:
  - 2 * 2
  - 2 - 3
  * $ \frac{7}{2} + 3 $
  - seven plus two
1#
```

Feedback flag **must** be the first one after question number.

## Question indicator ##
It is possible to put questions into two categories:

 - good question - `-` indicator,
 - good with small flaws - `~` indicator.

they need to be placed right after question definition; please see example below for usage.

```
#1 -
difficulty : easy
reference : 5.2
question:
  Which of the following is $\LaTeX$ equation?
image::
  img/unicorn.jpg
image: my caption :
  img/unicorn.jpg
// these are answers, a correct answer
// is indicated by a "*"
answers:single:
  - 2 * 2
  - 2 - 3
  * $ \frac{7}{2} + 3 $
  - seven plus two
1#

#3 ~
difficulty : hard
reference : 12.2
question:
  Order the following numbers:
answers:sort:
  2) 26
  1) 19
  3) 100
3#
```
