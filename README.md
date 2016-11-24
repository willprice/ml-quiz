# Quick quiz generator
A quick quiz generator focused on content; not platform.

To generate a quiz create a text file with extension `.quiz` in the root of this folder structure (where `README.md` is located).

Each quiz file must contain definition of:

 - `"candidate_number:"` - your University of Bristol candidate number (a 5-digit number that you can find on your SAFE profile page next to **Candidate** keyword) e.g. `"candidate_number": [12345]`; if you are working in a pair please expand the list appropriately e.g. `"candidate_number": [12345, 54321]`;
 - `"title:"` - the title of your quiz e.g. `"title": "Quick-quiz show-off."`;
 - `"url:"` - url to your quiz; if you host it on GitHub give a link to your GitHub repository otherwise put `"url": "127.0.0.1"`.

The syntax of the `.quiz` file closely follows `JSON` syntax. There are two enhancements though:

- comments in the quiz file are introduced in a single line starting with `//`;  
- strings can be multi-line by appending `\` at the very end of the line.

Each question is a `JSON` dictionary placed at the top level of the document with keyword being a string representing the number of the question. Numbers given to the questions don't have to be in order; they will be randomised before displaying.

## Question flags ##
### Required parameters ###
The following parameters are required for each question:

 - `"difficulty":` integer on a scale from 1 (very easy) to 5 (very hard), with the following meaning:
    * "1" - can be answered by looking up a specific passage in the book (e.g., match the following impurity measures with their mathematical definition); 
    * "2" - requires some straightforward reasoning or calculation (e.g., complete the following contingency table); 
    * "3" - requires more involved reasoning or calculation (e.g., a question involving some training data); 
    * "4" - requires reasoning beyond what was discussed in the lectures (e.g., material on starred slides such as kernel methods); 
    * "5" - a question on an advanced topic that was not discussed in the book (e.g., topics discussed in the epilogue).  
 - `"reference":` defines ML book chapter and section that the question corresponds to; it is given in format **chapter.section** e.g. `5.12`. If the question is beyond the scope of the book put `0` as the reference.
 - `"problem_type":` choose the most applicable one from the following list, or you can supply your own: 
    * "definition" - tests definitional knowledge;  
    * "calculation" - the answer needs to be derived by means of calculation;  
    * "problem-solving" - the question requires reasoning beyond calculation;  
    * "training" - the question is about training particular models;  
    * "evaluation" - the question is about evaluating particular models;  
 - `"answer_type":` defines type of the question; see section **Types of question** below for more details.
 - `"question":` defines the question text that will be displayed; both *in-line* LaTeX (i.e. `$\LaTeX$`) and *display* LaTeX (i.e. `$$\LaTeX$$`) are supported.
 - `"answers":` are answers to the question; each **correct** answer requires an `"explanation":` field, which explains why this particular answer is correct.
 - `"hint":` should provide a hint that helps solving the question.
 - `"workings":` show in detail how to arrive at the correct answer.
 - `"source":` is a reference to a book (with chapter and section) or a web page that inspired the question.
 - `"comments":` should briefly describe what knowledge it tests, and what your rationale for classifying it with given difficulty is. Additionally, you may want to include any other comments that might be relevant while marking the question.

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
Each type of the question needs properly formatted answers.  
For *single choice* questions the answer is defined by a list of dictionaries with `-` indicating all incorrect answers and `+` indicating a correct one, e.g.:
```
"answer_type": "single",
"answers": [
  { "correctness": "-",
    "answer": "False"
  },
  { "correctness": "-",
    "answer": "Another False"
  },
  { "correctness": "+",
    "answer": "True",
    "explanation": "why this answer is correct"
  },
  { "correctness": "-",
    "answer": "One more False"
  }
]
```
For the *multiple choice* follow the same strategy, but you can use multiple `+` indicators, e.g.:
```
"answer_type": "multiple",
"answers": [
  { "correctness": "-",
    "answer": "False"
  },
  { "correctness": "-",
    "answer": "Another False"
  },
  { "correctness": "+",
    "answer": "True",
    "explanation": "why this answer is correct"
  },
  { "correctness": "+",
    "answer": "One More True ",
    "explanation": "why this answer is correct"
  }
]
```
For *ordering questions* please specify the correct order with integers `1`, `2`, etc., e.g.:
```
"answer_type": "sort",
"answers": [
  { "correctness": "2",
    "answer": "This is the second element",
    "explanation": "why this order is correct"
  },
  { "correctness": "4",
    "answer": "This is the fourth element",
    "explanation": "why this order is correct"
  },
  { "correctness": "1",
    "answer": "This is the first element",
    "explanation": "why this order is correct"
  },
  { "correctness": "3",
    "answer": "This is the third element",
    "explanation": "why this order is correct"
  }
]
```
For the *filling-in blanks* question is defined as a list of *strings* (that will appear) and *integers* (blanks in the text that correspond to correct answer). `"answer:"` field is a list of dictionaries containing the missing text and blanks identifier, e.g.
```
"answer_type": "blank_answer",
"question": [
  "This ", 1, " will be asked. Same as ", 2, " one."
],
"answers": [
  { "correctness": 1,
    "answer": "word",
    "explanation": "why this answer is correct"
  },
  { "correctness": 2,
    "answer": "this,that",
    "explanation": "why this answer is correct"
  }
]
```
If more than one answer is correct please separate them by comma e.g. `blue,yellow,green`.  

For *filling-in contingency matrix* in the `"answers":` field is a dictionary of with the following elements:

- `"answer":` - a list, one string per row, formatted as shown below;
- `"explanation":` - gives reasoning behind the correct answer.

Here's an example:
```
"answer_type": "cloze_answer",
"answers": {
  "answer": ["1 | 4 | 5 ",
             "----------",
             "2 | 5 | 7 ",
             "----------",
             "3 | 9 | 12"],
  "explanation": "why this answer is correct"
}
```
Where the numbers are as follows:

|          | Predicted + | Predicted - |    |
|----------|-------------|-------------|----|
| Actual + | 1           | 4           | 5  |
| Actual - | 2           | 5           | 7  |
|          | 3           | 9           | 12 |

Finally, for *object matching* `"correctness":` is left part of the text, `"answer:` is the right part, `"explanation":` is the same as in the examples above, e.g.
```
"answer_type": "matrix_sort_answer",
"answers": [
  { "correctness": "The letter after 'a' is ",
    "answer": "'B'.",
    "explanation": "why this answer is correct"
  },
  { "correctness": "The letter after 'g' is ",
    "answer": "'H'.",
    "explanation": "why this answer is correct"
  },
  { "correctness": "I like ",
    "answer": "alphabet.",
    "explanation": "why this answer is correct"
  }
]
```

For more details please see `.quiz` file attached below.

## Restrictions ##
The `.quiz` files are translated into HTML with use of *regular expressions* and *JSON parsing*. This means that if any of your question does not follow the syntax rules it will be omitted. Most of the time you will get an error message, which should be self explanatory. Unfortunately, regex matcher cannot produce any error messages therefore some mistakes may cause a question to fail quietly.

To make sure that your questions get compiled please follow the example given below as close as possible.  
As most of the keywords and answers will be placed as a string in the quiz file **any special character must be escaped**.  
Finally, your quiz file must have `.quiz` extension and need to be placed in the root folder of this repository.

The quiz compiler requires `Python 2.x` and works on most Linux (2.11MVB machines) and Unix (OS X) machines.

## Syntax ##
As the quiz file is translated into HTML the questions and answers support HTML tags e.g. `<br>` for new line; feel free to use them but please avoid complicated structures.

Moreover, both *in-line* LaTeX (introduced by `$` environment e.g. `$\LaTeX$`) and *display* LaTeX (introduced by `$$` environment e.g. `$$\LaTeX$$`) are supported.

## Online quiz example ##
See an [example quiz](http://so-cool.github.io/quick-quiz/my_quiz.html).

## Not compiling questions ##
If your question is not compiling and you have followed all the guidelines given in this document you can email me for help.  
The recommended approach for developing your questions is one question per file during their creation, and then combining them into one file before submission.

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
    "difficulty": "1",
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
        "answer": "2 * 2"
      },
      { "correctness": "-",
        "answer": "2 - 3"
      },
      { "correctness": "+",
        "answer": "$\\frac{7}{2} + 3$",
        "explanation": "why this answer is correct"
      },
      { "correctness": "-",
        "answer": "seven plus two"
      }
    ],
    "hint": "you do the math",
    "workings": "how to arrive at the correct answer and why all the others are incorrect",
    "source": "wikipedia url",
    "comments": "What's special about this question?"
  },

  "2": {
    "difficulty": "5",
    "reference": "2.2",
    "problem_type": "calculations",
    "question": "Mark all the letters:",
    "answer_type": "multiple",
    "answers": [
      { "correctness": "+",
        "answer": "T",
        "explanation": "why this answer is correct"
      },
      { "correctness": "+",
        "answer": "F",
        "explanation": "why this answer is correct"
      },
      { "correctness": "-",
        "answer": "7"
      },
      { "correctness": "-",
        "answer": "<img src=\"img/unicorn.jpg\" style=\"width:304px;height:228px;\">"
      },
      { "correctness": "+",
        "answer": "W",
        "explanation": "why this answer is correct"
      }
    ],
    "hint": "you do the alphabet",
    "workings": "how to arrive at the correct answer and why all the others are incorrect",
    "source": "some book",
    "comments": "What's special about this question?"
  },

  "3": {
    "difficulty": "2",
    "reference": "12.2",
    "problem_type": "beyond scope of the book",
    "question": "Order the following numbers:",
    "answer_type": "sort",
    "answers": [
      { "correctness": "2",
        "answer": "26",
        "explanation": "why this order is correct"
      },
      { "correctness": "1",
        "answer": "19",
        "explanation": "why this order is correct"
      },
      { "correctness": "3",
        "answer": "70",
        "explanation": "why this order is correct"
      }
    ],
    "hint": "you do the alphabet",
    "workings": "how to arrive at the correct answer and why all the others are incorrect",
    "source": "some book",
    "comments": "What's special about this question?"
  },

  "4": {
    "difficulty": "4",
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
        "explanation": "why this answer is correct"
      },
      { "correctness": 2,
        "answer": "red",
        "explanation": "why this answer is correct"
      }
    ],
    "hint": "you do the alphabet",
    "workings": "how to arrive at the correct answer and why all the others are incorrect",
    "source": "some book",
    "comments": "What's special about this question?"
  },

  "5": {
    "difficulty": "3",
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
      "explanation": "why this answer is correct"
    },
    "hint": "you do the alphabet",
    "workings": "how to arrive at the correct answer and why all the others are incorrect",
    "source": "some book",
    "comments": "What's special about this question?"
  },

  "6": {
    "difficulty": "5",
    "reference": "3.3",
    "problem_type": "beyond scope of the book",
    "question": "Match the following sentences.",
    "answer_type": "matrix_sort_answer",
    "answers": [
      { "correctness": "The letter after 'a' is ",
        "answer": "'B'.",
        "explanation": "why this answer is correct"
      },
      { "correctness": "The letter after 'g' is ",
        "answer": "'H'.",
        "explanation": "why this answer is correct"
      },
      { "correctness": "I like ",
        "answer": "alphabet.",
        "explanation": "why this answer is correct"
      }
    ],
    "hint": "you do the alphabet",
    "workings": "how to arrive at the correct answer and why all the others are incorrect",
    "source": "some book",
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
  -q #Q, --question #Q  the # of question to be generated (all questions are
                        generated by default)
  -a, --all             generate all of the questions
  -s, --separate        generate all of the questions in separate files
  -i, --iframe          generate all of the question on one page (iframe)
  -o, --order           order the questions first on book section then on
                        difficulty
  -O, --Order           order the questions first on difficulty then on
                        book section
  -d, --debug           indicate the correct answer in the question
  --comments            show *comments* in each question
  --hints               show *hints* in each question
  --source              show *source* in each question
  --workings            show *workings* in each question
  --explanation         show *explanation* in each answer
  -c, --count           show difficulty statistics of the quiz file
  -t, --tarball         tarball the quiz for submissions
```

Therefore, flag `-a` compiles all of the questions in given `.quiz` file into one HTML. `-q 7` compiles only question `#7`. `-s` will compile all of the questions and place each one in a separate HTML file. `-i` generates `iframe` based HTML displaying all questions on a single web page.  
`-d` will generate an HTML with correct answers indicated by *chevron* symbol - really useful feature for questions development. `-c` will produce question difficulty statistics; and `-o`/`-O` will create additional `.quiz` file with questions sorted as described above. `--comments`, `--hints`, `--source`, `--workings` and `--explanation` will display respectively comments, hints, source, workings and explanation in the rendered HTML.  
Finally, `-t` creates a *tarball* (archive) with all the files necessary for submission.

# Submission #
Please submit only a tarball with your quiz created with `-t` option. Your submission will primarily be marked on the diversity and originality of your questions, as well as your assessment of their difficulty level.

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
