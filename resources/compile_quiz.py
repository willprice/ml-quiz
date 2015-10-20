#!/usr/bin/env python

import re
import sys, os
import json

#
# find all questions and metadata
#
q_rx = re.compile(r"""
  # number of the question
  (?P<number>\d+)\)
  # Question being asked
  (?P<prompt>.+\?)
  # Possible answers to the question
  (?P<answers>(?:\s+[-\*]\s.+)+)
  # image to include in response
  \s+(?P<image>\(image\).+)?
  # Extra text to include in response
  \s+(?P<text>(?![-\*]|^\d+\)|\s+\(image\)).+)?
""", re.X | re.M)

#
# question answer regex
#
answ_rx = re.compile(r"""
  # indicator if correct or not
  #
  # (-) : incorrect
  # (*) : correct
  #
  \s+(?P<correct>[-\*])
  # actual text of answer
  \s+(?P<answer>.+)
""", re.X | re.M)

def toJson(filename):
  with open(filename, 'r') as quiz_file:
    quiz_text = quiz_file.read()

  # find the parent url before comments are removed
  url = re.search(r'^url:(.+)', quiz_text, re.M)
  if url:
    url = url.group(1).strip()

  # find title for quiz
  title = re.search(r'^#(.+)', quiz_text, re.M)
  if title:
    title = title.group(1).strip()

  # remove comments from quiz file
  quiz_text = re.sub(r'//(.+)', "", quiz_text)

  # find all questions
  questions = [m.groupdict() for m in q_rx.finditer(quiz_text)]

  results = []

  for q in questions:

    out = {}

    out['prompt'] = q['prompt'].strip()
    out['number'] = int(q['number'])

    if q['image']:
      out['image'] = q['image'].replace('(image)', "").strip()

    # correct answer info
    out['correct'] = {}

    if q['text']:
      out['correct']['text'] = q['text'].strip()

    answers = [m.groupdict() for m in answ_rx.finditer(q['answers'])]

    out['answers'] = []
    for i, a in enumerate(answers):
      out['answers'].append(a['answer'].strip())
      if a['correct'] == "*":
        out['correct']['index'] = i

    results.append(out)

  with open(filename[:-5] + ".json", 'w') as outfile:
    json.dump(
      {
        "questions" : sorted(results, key=lambda x: x['number']),
        "title" : title,
        "url" : url
      },
      outfile,
      sort_keys=True,
      indent=2,
      separators=(',', ': ')
    )

#
# update filename in index.html
#
def updateIndex(dirname, jsonPath):
  # prepare JSON filename i.e. remove directories just leave filename
  jsonName = None
  jsonName_i = jsonPath[::-1].find('/')
  if jsonName_i == -1:
    jsonName = jsonPath
  else:
    jsonName =jsonPath[::-1][:jsonName_i][::-1]

  with open(dirname + "index.html", 'w') as writer:
    with open(dirname + "resources/index.html", 'r') as reader:
      for line in reader:
        writer.write(line.replace("my_quiz.json", jsonName))

if __name__ == '__main__':
  if len(sys.argv) == 1:
    print("no quiz file given...")
  else:
    quizFilename = sys.argv[1]
    if os.path.exists(quizFilename):
      if os.path.isfile(quizFilename):
        if quizFilename[-5:] != ".quiz":
          print("Your file must have `.quiz` extension")
          sys.exit(1)
      else:
        print(quizFilename + " is not a file!")
        sys.exit(1)
    else:
      print(quizFilename + " does not exist!")
      sys.exit(1)

    quizJson = quizFilename[:-5] + ".json"
    print("generating " + quizJson)
    toJson(quizFilename)

    indexFilename = None
    indexDir_i = quizFilename[::-1].find('/')
    if indexDir_i != -1:
      indexDir = quizFilename[::-1][indexDir_i:][::-1]
    else:
      indexDir = "./"
    indexFilename = indexDir + "index.html"
    print("updating " + indexFilename)
    updateIndex(indexDir, quizJson)
