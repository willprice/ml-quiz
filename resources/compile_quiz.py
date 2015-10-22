#!/usr/bin/env python

import re
import sys, os
import json

#
# find all questions and metadata
#
q_rx = re.compile(r"""
  # number of the question
  \s*\#\s*(?P<number>\d+)\s*
  # question difficulty
  (difficulty)\s*:\s*(?P<difficulty>(easy)|(medium)|(hard))\s*
  # question reference
  (reference)\s*:\s*(?P<chapter>\d+)\.(?P<section>\d+)\s*
  # Question being asked
  (question)\s*:\s*(?P<prompt>.+)\s*
  # image(s) to include in response
  (?P<images>(\s*(image)\s*:.*:.*\s*)*)
  # Possible answers to the question
  (answers)\s*:\s*(?P<answer_type>(single)|(multi)|(order)|(blanks))\s*:(?P<answers>(?:\s*(\-|\*|(\d+\s*\)))\s*.+)*)\s*
  # Extra text to include in response
  ((response)\s*:\s*(?P<text>.+))?\s*
  \s*(?P=number)\s*\#\s*
""", re.X | re.M)

#
# image regex
#
#
img_rx = re.compile(r"""
  \s*(image)\s*:\s*(?P<caption>.*)\s*:\s*(?P<path>.+)\s*
""", re.X | re.M)

#
# fill in blanks regex
#
blanks_rx = re.compile(r"""
  (?P<text>[^\[\]]+)?
  (\[(?P<blank>[^\]]+)\])?
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
  # or ordering of the answers
  # eg. 1) 2) 3)
  #
#  \s*(?P<correct>[-*])
  \s*(?P<correct>\-|\*|(\d+\s*\)))
  # actual text of answer
  \s*(?P<answer>.+)\n
""", re.X | re.M)

def toJson(filename):
  with open(filename, 'r') as quiz_file:
    quiz_text = quiz_file.read()

  # find the parent url before comments are removed
  url = re.search(r'^url:(.+)', quiz_text, re.M)
  if url:
    url = url.group(1).strip()

  # find title for quiz
  title = re.search(r'^title:(.+)', quiz_text, re.M)
  if title:
    title = title.group(1).strip()

  # find user id
  uid = re.search(r'^uid:(.+)', quiz_text, re.M)
  if uid:
    uid = uid.group(1).strip()

  # remove comments from quiz file
  quiz_text = re.sub(r'//(.+)', "", quiz_text)

  # find all questions
  questions = [m.groupdict() for m in q_rx.finditer(quiz_text)]

  results = []
  question_indeces = []

  for q in questions:

    out = {}

    try:
      out['number'] = int(q['number'])
    except:
      print("Question number not given")
      sys.exit(1)
    if out['number'] in question_indeces:
      print("Question index: " + str(out['number'] + " repeated"))
      sys.exit(1)
    question_indeces.append(out['number'])

    try:
      out['answer_type'] = q['answer_type'].strip()
    except:
      print("Answer type (single, multi, etc.) not given for question #" + str(out['number']))
      sys.exit(1)

    try:
      out['chapter'] = int(q['chapter'])
    except:
      print("Chapter number not given in question #" + str(out['number']))
      sys.exit(1)

    try:
      out['section'] = int(q['section'])
    except:
      print("Section number not given in question #" + str(out['number']))
      sys.exit(1)

    try:
      out['difficulty'] = q['difficulty'].strip()
    except:
      print("Difficulty not given in question #" + str(out['number']))
      sys.exit(1)

    try:
      if out['answer_type'].lower() == 'blanks':
        prompt = [m.groupdict() for m in blanks_rx.finditer(q['prompt'].strip())]
        out['prompt'] = []
        out['correct'] = []
        for a in prompt:
          if a['text']:
            out['prompt'].append(a['text'])
          if a['blank']:
            out['prompt'].append(len(out['correct']))
            out['correct'].append(a['blank'])
      else:
        out['prompt'] = q['prompt'].strip()
        out['answers'] = []
        out['correct'] = []
        try:
          answers = [m.groupdict() for m in answ_rx.finditer(q['answers'].strip()+"\n")]
        except:
          print("Answers not given or malformed for question #" + str(out['number']))
          sys.exit(1)
        for i, a in enumerate(answers):
          out['answers'].append(a['answer'].strip())
          if a['correct'] == "*":
            out['correct'].append(i)
          elif ')' in a['correct']:
            out['correct'].append( int(a['correct'].strip().strip(')').strip())  )
    except:
      print("Question not given in question #" + str(out['number']))
      sys.exit(1)

    if q['images']:
      images = [m.groupdict() for m in img_rx.finditer(q['images'].strip())]
      out['captions'] = []
      out['images'] = []
      for a in images:
        out['captions'].append(a['caption'].strip())
        out['images'].append(a['path'].strip())

    # TODO: add possibility to attach image in the answer
    if q['text']:
      out['text'] = q['text'].strip()

    results.append(out)

  with open(filename[:-5] + ".json", 'w') as outfile:
    json.dump(
      {
        "questions" : sorted(results, key=lambda x: x['number']),
        "title" : title,
        "url" : url,
        "uid" : uid
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
