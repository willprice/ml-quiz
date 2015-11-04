#!/usr/bin/env python

import re
import sys, os
import json
from html_templates import questionCategories,questionTemplate,quizTemplate
from html_templates import singleTemplate
from html_templates import sortTemplate
from html_templates import matrixSort_answers_single,matrixSort_question_single,matrixSort_questionTemplate
from html_templates import tableTemplate
from html_templates import blankItem,blankTemplate
from html_templates import multipleTemplate

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
  (?P<images>(\s*(image)\s*:.*:\s*\n\s*.*\s*\n)*)
  # Possible answers to the question
  (answers)\s*:\s*(?P<answer_type>(single)|(multiple)|(sort)|(blank_answer))\s*:(?P<answers>(?:\s*(\-|\*|(\d+\s*\)))\s*.+)*)\s*
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

# debug answers
ANSWERS_DEBUG = True#False

#
# correct answer indicator
#
def markAnswer(answerText):
  return "&laquo;" + " " + answerText
def markAnswer(answerText, order):
  return str(order) + "" + "&laquo;" + " " + answerText
def markBlank(answerText):
  return "&raquo;" + answerText + "&laquo;" + " "

#
# blanks converter
#
def mergeBlanks(textList, answers):
  answer = ""
  for i in textList:
    if type(i) == int:
      answer += "[answer]" + answers[i] + "[/answer]"
    elif type(i) == str:
      answer += i
    else:
      print( "Unknown prompt type!" )
      sys.exit(1)
  return answer
def fillBlanks(textList, dictionaryAnswers):
  qs = ""
  for i in textList:
    if type(i) == int:
      qs += ( blankItem % dictionaryAnswers[i] )
    elif type(i) == str:
      qs += i
    else:
      print( "Unknown prompt type!" )
      sys.exit(1)
  return qs

def parseQuestions(filename):
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
      if out['answer_type'].lower() == 'blank_answer':
        prompt = [m.groupdict() for m in blanks_rx.finditer(q['prompt'].strip())]
        out['prompt'] = []
        out['correct'] = []
        for a in prompt:
          if a['text']:
            out['prompt'].append(a['text'])
          if a['blank']:
            if ANSWERS_DEBUG:
              out['prompt'].append(markBlank(a['blank']))
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
            # if answer debug flag is set append correct answer indicator
            if ANSWERS_DEBUG:
              out['answers'][i] = markAnswer(out['answers'][i])
          elif ')' in a['correct']:
            out['correct'].append( int(a['correct'].strip().strip(')').strip())  )
            # if answer debug flag is set append correct ordering
            if ANSWERS_DEBUG:
              out['answers'][i] = markAnswer(out['answers'][i], out['correct'][-1])
    except:
      print("Question not given in question #" + str(out['number']))
      sys.exit(1)

    out['captions'] = []
    out['images'] = []
    if q['images']:
      images = [m.groupdict() for m in img_rx.finditer(q['images'].strip())]

      for a in images:
        out['captions'].append(a['caption'].strip())
        out['images'].append(a['path'].strip())

    # TODO: add possibility to attach image in the answer
    if q['text']:
      out['text'] = q['text'].strip()

    results.append(out)

  return(results, title, url, uid)

# return HTML image environment
def insertImage(path, caption):
  return "<br><figure><img src=\"" + path + "\" /><figcaption>" + caption + "</figcaption></figure>"

# This function generates the JSON code that is required for the quiz
# library to grade the quizzes
def htmlToJson(question):
  json = {
    "type"   : question["answerType"],
    "id"     : question["id"],
    "catId"  : 0,
    "points" : 1,
    "correct": question["correctness"]
  }
  return json

# prepare and write results to html file
def toHtml(filename, results, title):
  questions = []
  jsons = {}

  for result in results:
    question = {}
    question["questionNumber"] = question["id"] = result['number']
    question["category"]       = str(result['chapter']) + "." + str(result['section']) +\
      ": " +  questionCategories[result['chapter']][0] + " : " + questionCategories[result['chapter']][result['section']]
    question["difficulty"]     = result['difficulty']

    # prepare question to display: text + images
    question["question"]       = result['prompt']
    for i in range(len(result['images'])):
      question["question"] += insertImage(result['images'][i], result['captions'][i])

    if result['answer_type'] == 'single':
      # Loop over the answers and extract the text if it has been filled in appropriately
      # remodel answers so that the first one in the list is correct
      # TODO: fix in the same way as in multiple answers
      rAnswers = result['answers'][:]
      rAnswers_c = rAnswers.pop(result['correct'][0])
      rAnswers.insert(0, rAnswers_c)
      answers = []
      for ai, answer in enumerate(rAnswers):
        answers.append( dict(
          answerPos_0 = ai,
          answerPos_1 = ai + 1,
          id = question["id"],
          answerText = answer) )

      question["answers"] = answers

      question["correctness"] = [0] * len( question["answers"] )
      question["correctness"][0] = 1

      question["answersStr"] = "\n".join( singleTemplate % answer for answer in answers )
      question["numAnswers"] = len( answers )
      question["answerType"] = result['answer_type']
      question["json"] = htmlToJson( question )
      question["questionHTML"] = questionTemplate % question
    elif result['answer_type'] == 'multiple':
      answers = []
      for ai, answer in enumerate(result['answers']):
        answers.append( dict(
          answerPos_0 = ai,
          answerPos_1 = ai + 1,
          id = question["id"],
          answerText = answer) )
      question["answers"] = answers

      question['correctness'] = [0] * len( question["answers"] )
      for ri in result['correct']:
        question["correctness"][ri] = 1

      question["answersStr"] = "\n".join( multipleTemplate% answer for answer in answers )
      question["numAnswers"] = len( answers )
      question["answerType"] = result['answer_type']
      question["json"] = htmlToJson( question )
      question["questionHTML"] = questionTemplate % question
    elif result['answer_type'] == 'sort':
      answers = []
      for ai, answer in enumerate(result['answers']):
        answers.append( dict(
          answerPos_0 = ai,
          answerPos_1 = ai + 1,
          id = question["id"],
          answerText = answer) )
      question["answers"] = answers

      question["correctness"] = result['correct']

      question["answersStr"] = "\n".join( sortTemplate% answer for answer in answers )
      question["numAnswers"] = len( answers )
      question["answerType"] = result['answer_type']
      question["json"] = htmlToJson( question )
      question["questionHTML"] = questionTemplate % question
    elif result['answer_type'] == 'blank_answer':
      # overwrite the question prompt
      question["question"] = "Fill in the blanks"
      question["rawQuestion"] = mergeBlanks(result['prompt'], result['correct'])

      # Build up the dictionary of answers
      question["answers"] = []
      question["correctness"] = []
      for ic in result['correct']:
        ic_r = ic.split(',')
        ic_r = [r.strip() for r in ic_r]
        question["correctness"].append(ic_r)
        question["answers"].append({'length':max(map(len,ic_r)), 'answers':"("+', '.join(ic_r)+")"})

      questionStr = fillBlanks(result['prompt'], question["answers"])

      question["answerType"] = result['answer_type']
      question["numAnswers"] = len( question["answers"] )
      question["json"] = htmlToJson( question )
      question["answersStr"] = str( blankTemplate % questionStr )

      question["questionHTML"] = questionTemplate % question
    elif result['answer_type'] == 'matrix_sort_answer':
      pass
    elif result['answer_type'] == 'cloze_answer':
      pass
    else:
      print( "Question type not recognised: " + result['answer_type'] + " !" )
      sys.exit(1)

    jsons[str( question["id"] )] = question["json"]
    questions.append( question["questionHTML"] )

  quiz = dict( \
    quizTitle = title,
    questions = '\n'.join( questions ),
    answersJSON = jsons )

  with open(filename[:-5] + ".html", 'w') as outfile:
    outfile.write(quizTemplate % quiz)

def toJson(filename, results, title, url, uid):
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

    results, title, url, uid = parseQuestions(quizFilename)
    toHtml(quizFilename, results, title)

#     quizJson = quizFilename[:-5] + ".json"
    # print("generating " + quizJson)
    # results, title, url, uid = parseQuestions(quizFilename)
    # toJson(quizFilename, results, title, url, uid)

    # indexFilename = None
    # indexDir_i = quizFilename[::-1].find('/')
    # if indexDir_i != -1:
      # indexDir = quizFilename[::-1][indexDir_i:][::-1]
    # else:
      # indexDir = "./"
    # indexFilename = indexDir + "index.html"
    # print("updating " + indexFilename)
    # updateIndex(indexDir, quizJson)
