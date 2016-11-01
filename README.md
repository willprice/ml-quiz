# Quick quiz generator
A quick quiz generator focused on content; not platform.

To generate a quiz create a text file with `.quiz` extension in the root of this folder structure (where `README.md` is located).

Each quiz file must contain definition of:

 - `"candidate_number:"` - your University of Bristol candidate number e.g. `"candidate_number": [12345]`, if more than one person is working on a quiz please expand the list appropriately e.g. `"candidate_number": [12345, 54321]`;
 - `"title:"` - the title of your quiz e.g. `"title": "Quizk-quiz show-off."`;
 - `"url:"` - url to your quiz; if you host it on GitHub give a link to your GitHub repository otherwise put `"url": "127.0.0.1"`.

The syntax of the `.quiz` file closely follow the one of `JSON`. There are two enhancements though:

- comments in the quiz file are introduced in a single line starting with `//`;  
- strings can be multi-line by appending `\` at the very end of the line.

Each question is a dictionary placed at the top level of the document with keyword being string representing the number of the question. Numbers given to the questions don't have to be in order; they will be randomised before displaying.

## Question flags ##
### Required parameters ###
The following parameters are required for each question:

 - `"difficulty":` defines difficulty of the questions; possibilities are: **easy**, **medium** and **hard**.
 - `"reference":` defines ML book chapter and section that the question corresponds to; it is given in format **chapter<dot>section** e.g. `5.12`.
 - `"problem_type":` is a brief description of the problem e.g. **definition**, **calculations**; this is entirely up to you.
 - `"answer_type":` defines type of the question; see section **Types of question** below for more details.
 - `"question":` defines the question text that will be displayed; both *in-line* LaTeX (i.e. `$\LaTeX$`) and *display* LaTeX (i.e. `$$\LaTeX$$`) are supported.
 - `"answers":` are answers to the question; each answer requires a `"hint":` which should explain why this particular answer is correct or incorrect, and optionally `"comments":` if you fill that some more explanation is necessary.

### Optional parameters ###
You can optionally attach image(s) to your question with `"images":` field being a list of dictionaries, each containing `"url":` and *optionally* `"caption":`, e.g.
```
"images": [
  {"url": "path/to/my/image.jpg",
   "caption": "my caption"}
]
```

## Types of question ##
You can specify the following types of question:

 - Single choice (`single` keyword)
 - Multiple choice (`multiple` keyword)
 - Order elements (`sort` keyword)
 - Fill in blanks (`blank_answer` keyword)
 - Fill in contingency matrix (`cloze_answer` keyword)
 - Match objects (`matrix_sort_answer` keyword)

You define the type of a question with `"answer_type":` keyword e.g. `"answer_type": "single"` - see the example attached below for more details.

### Specifying answer to each type of question ###
Each type of the question needs properly formated answers.  
For *single choice* questions the answer is defined by a list of dictionaries with `-` marking incorrect answer and `+` indicating the correct one, e.g.:
```
"answer_type": "single",
"answers": [
  { "correctness": "-",
    "answer": "False",
    "hint": "Just because it's False",
    "comments": ""
  },
  { "correctness": "-",
    "answer": "Another False",
    "hint": "Just because it's False",
    "comments": ""
  },
  { "correctness": "+",
    "answer": "True",
    "hint": "Just because it's True",
    "comments": ""
  },
  { "correctness": "-",
    "answer": "One more False",
    "hint": "Just because it's False",
    "comments": ""
  }
]
```
For the *miltiple choice* follow the same strategy but with multiple `+` indicators, e.g.:
```
"answer_type": "multiple",
"answers": [
  { "correctness": "-",
    "answer": "False",
    "hint": "Just because it's False",
    "comments": ""
  },
  { "correctness": "-",
    "answer": "Another False",
    "hint": "Just because it's False",
    "comments": ""
  },
  { "correctness": "+",
    "answer": "True",
    "hint": "Just because it's True",
    "comments": ""
  },
  { "correctness": "+",
    "answer": "One More True ",
    "hint": "Just because it's True",
    "comments": ""
  }
]
```
For *ordering questions* please specify the correct order with integers `1`, `2`, etc., e.g.:
```
"answer_type": "sort",
"answers": [
  { "correctness": "2",
    "answer": "This is the second element",
    "hint": "second = 2",
    "comments": ""
  },
  { "correctness": "4",
    "answer": "This is the fourth element",
    "hint": "fourth = 4",
    "comments": ""
  },
  { "correctness": "1",
    "answer": "This is the first element",
    "hint": "first = 1",
    "comments": ""
  },
  { "correctness": "3",
    "answer": "This is the third element",
    "hint": "third = 3",
    "comments": ""
  }
]
```
For the *filling-in blanks* question is defined as a list of *strings* (that will appear) and *integers* (blanks in the text that correspond to correct answer). `"answer:"` field is a list of dictionaries containing the missing text and blank identifier, e.g.
```
"answer_type": "blank_answer",
"question": [
  "This ", 1, " will be asked. Same as ", 2, " one."
],
"answers": [
  { "correctness": 1,
    "answer": "word",
    "hint": "just the WORD",
    "comments": ""
  },
  { "correctness": 2,
    "answer": "this,that",
    "hint": "it's obvious, isn't it?",
    "comments": ""
  }
]
```
If more than one answer is correct please separate them by comma e.g. `blue,yellow,green`.  

For *filling-in contingency matrix* in the `"answers":` field is a dictionary of with the following elements:

- `"answer":` - a list, one string per row, formated as shown below;
- `"hint":` - same as above;
- `"comments":` - same as above.

Here's an example:
```
"answer_type": "cloze_answer",
"answers": {
  "answer": ["1 | 4 | 5 ",
             "----------",
             "2 | 5 | 7 ",
             "----------",
             "3 | 9 | 12"],
  "hint": "1+4=5; 2+5=7; 3+9=12; etc.",
  "comments": "just do the math"
}
```
Where the numbers are as follows:

|          | Predicted + | Predicted - |    |
|----------|-------------|-------------|----|
| Actual + | 1           | 4           | 5  |
| Actual - | 2           | 5           | 7  |
|          | 3           | 9           | 12 |

Finally, for *object matching* `"correctness":` is left part of the text and `"answer:` is the right part, e.g.
```
"answer_type": "matrix_sort_answer",
"answers": [
  { "correctness": "The letter after 'a' is ",
    "answer": "'B'.",
    "hint": "go through the alphabet",
    "comments": ""
  },
  { "correctness": "The letter after 'g' is ",
    "answer": "'H'.",
    "hint": "go through the alphabet",
    "comments": ""
  },
  { "correctness": "I like ",
    "answer": "alphabet.",
    "hint": "the bird is the word",
    "comments": ""
  }
]
```

For more details please see `.quiz` file attached below.

## Restrictions ##
The `.quiz` files are compiled to HTML with use of *regular expressions* and *JSON parsing*. This means that if any of your question does not follow the syntax rules it will be omitted. Most of the time you will get an error mesage which should be self explanatory. Unfortunately, regex matcher cannot produce any error messages therefore some mistakes may cause a question to fail quietly.

To make sure that your questions get compiled please follow the example given below as close as possible.  
As most of the keywords and answers will be placed as a string in the quiz file any special character must be escaped.  
Finally, your quiz file must have `.quiz` extension and need to be placed in the root folder of this repository.

The quiz compiler requires `Python 2.x` and works on Linux (2.11MVB machines) and Unix (OS X).

## Syntax ##
As the quiz file is translated into HTML the questions and answers support HTML tags e.g. `<br>` for new line; feel free to use them but please avoid complicated structures.

Moreover, both *in-line* LaTeX (introduced by `$` environment e.g. `$\LaTeX$`) and *display* LaTeX (introduced by `$$` environment e.g. `$$\LaTeX$$`) are supported.

## Online quiz example ##
See an [example quiz](http://so-cool.github.io/quick-quiz/my_quiz.html).

## Not compiling questions ##
If your question is not compiling and you have followed all the rules given in this document you can email me for help.  
The recommended approach to developing your questions is one question per file during their creation and then combining them into one file before submission.

# Usage #
## Create `.quiz` file ##
First, create a quiz text file using the following format (named `my_quiz.quiz` for example):

```
{
  // example quiz text
  // <- (this is a comment and will be ignored)

  // this is the url for your quiz
  "url": "http://so-cool.github.io/quick-quiz/",

  // this are your UoB candidate numbers as a comma separated list
  "candidate_number": [12345, 54321],

  // this is the title of the quiz
  "title": "Quizk-quiz show-off.",

  // this is an example question.
  // the number signifies the question order,
  // meaning questions can be placed in random order
  // within the file
  "1": {
    "difficulty": "easy",
    "reference": "5.2",
    "problem_type": "definitions",
    "question": "Which of the following is $\\LaTeX$ \
                 equation\
                 ?",
    "images": [
      { "url": "img/unicorn.jpg",
        "caption": "my caption"
      },
      { "url": "img/unicorn.jpg"}
    ],
    // these are answers, a correct answer
    // is indicated by a "+", incorrect answer has a "-"
    "answer_type": "single",
    "answers": [
      { "correctness": "-",
        "answer": "2 * 2",
        "hint": "",
        "comments": ""
      },
      { "correctness": "-",
        "answer": "2 - 3",
        "hint": "",
        "comments": ""
      },
      { "correctness": "+",
        "answer": "$\\frac{7}{2} + 3$",
        "hint": "",
        "comments": ""
      },
      { "correctness": "-",
        "answer": "seven plus two",
        "hint": "",
        "comments": ""
      }
    ],
    "comments": "What's special about this question?"
  },

  "2": {
    "difficulty": "medium",
    "reference": "2.2",
    "problem_type": "calculations",
    "question": "Mark all the letters:",
    "answer_type": "multiple",
    "answers": [
      { "correctness": "+",
        "answer": "T",
        "hint": "",
        "comments": ""
      },
      { "correctness": "+",
        "answer": "F",
        "hint": "",
        "comments": ""
      },
      { "correctness": "-",
        "answer": "7",
        "hint": "",
        "comments": ""
      },
      { "correctness": "-",
        "answer": "<img src=\"img/unicorn.jpg\" style=\"width:304px;height:228px;\">",
        "hint": "",
        "comments": ""
      },
      { "correctness": "+",
        "answer": "W",
        "hint": "",
        "comments": ""
      }
    ],
    "comments": "What's special about this question?"
  },

  "3": {
    "difficulty": "hard",
    "reference": "12.2",
    "problem_type": "beyond scope of the book",
    "question": "Order the following numbers:",
    "answer_type": "sort",
    "answers": [
      { "correctness": "2",
        "answer": "26",
        "hint": "",
        "comments": ""
      },
      { "correctness": "1",
        "answer": "19",
        "hint": "",
        "comments": ""
      },
      { "correctness": "3",
        "answer": "70",
        "hint": "",
        "comments": ""
      }
    ],
    "comments": "What's special about this question?"
  },

  "4": {
    "difficulty": "hard",
    "reference": "3.3",
    "problem_type": "beyond scope of the book",
    "answer_type": "blank_answer",
    "question": [
      "$2+2$ is ", 1, ". ",
      "What colour is a red truck: ", 2, "."
    ],
    "answers": [
      { "correctness": 1,
        "answer": "4",
        "hint": "",
        "comments": ""
      },
      { "correctness": 2,
        "answer": "red",
        "hint": "",
        "comments": ""
      }
    ],
    "comments": "What's special about this question?"
  },

  "5": {
    "difficulty": "hard",
    "reference": "3.3",
    "problem_type": "beyond scope of the book",
    "question": "Fill in contingency matrix.<br><br>1TP<br>5TN<br>12 in total<br>5 actual positive",
    "answer_type": "cloze_answer",
    "answers": {
      "answer": ["1 | 4 | 5 ",
                 "----------",
                 "2 | 5 | 7 ",
                 "----------",
                 "3 | 9 | 12"],
      "hint": "",
      "comments": ""
    },
    "comments": "What's special about this question?"
  },

  "6": {
    "difficulty": "hard",
    "reference": "3.3",
    "problem_type": "beyond scope of the book",
    "question": "Match the following sentences.",
    "answer_type": "matrix_sort_answer",
    "answers": [
      { "correctness": "The letter after 'a' is ",
        "answer": "'B'.",
        "hint": "",
        "comments": ""
      },
      { "correctness": "The letter after 'g' is ",
        "answer": "'H'.",
        "hint": "",
        "comments": ""
      },
      { "correctness": "I like ",
        "answer": "alphabet.",
        "hint": "",
        "comments": ""
      }
    ],
    "comments": "What's special about this question?"
  }
}

```

## Compiler usage ##
Then, parse it into an HTML file with:
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

Therefore, flag `-a` compiles all of the questions in given `.quiz` file into one HTML. `-q 7` compiles only question `#7`. `-s` will compile all of the questions and place each one in a separate HTML file. `-i` generates `iframe` based HTML displaying all questions on a single page.  
`-d` will generate an HTML with correct answers indicated by *chevron* symbol - really useful feature for questions development. `-c` will produce question difficulty statistics. And `-o`/`-O` will create additional `.quiz` file with questions sorted as described above.  
Finally, `-t` creates a *tarball* (archive) with all files necessary for submission.

# Submission #
Please submit only the following files:

- A tarball with your quiz created with `-t` option.
- `"command":` (**compulsory**) field in each question should briefly describe what knowledge it tests, and what your rationale for classifying it as easy/medium/hard is. Your submission will primarily be marked on the diversity and originality of your questions, as well as your assessment of their difficulty level.
    * An easy question is one that can be answered by looking up a specific passage in the book;
    * a medium question is one that requires some degree of problem-solving;
    * a hard question is one that requires some thinking beyond what was discussed in the lectures.

Finally, `"hint":` field for each answer is **compulsory** as well and marks will be cut for not including it.

# Assignment description #
Full assignment description is available [here](https://github.com/So-Cool/quick-quiz/wiki/Option-3:-ML-Quiz).

# Marking - markers only #
**Please do not use these options!**

**TO BE UPDATED**

## Feedback ##
**TO BE UPDATED**

## Question quality ##
**TO BE UPDATED**

## Mark ##
**TO BE UPDATED**
