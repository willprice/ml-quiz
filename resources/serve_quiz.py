#!/usr/bin/env python

import sys, os
import time
import argparse
import hashlib
import SocketServer, SimpleHTTPServer
from multiprocessing import Process
#
from compile_quiz import toJson, updateIndex

# default server port
PORT = "8888"

parser = argparse.ArgumentParser(description='Simple quiz generator that is served over http.')
parser.add_argument('-p', '--port', type=int, nargs=1, required=False, default=PORT, help=('port used by HTTP server (' + str(PORT) + ' by default)'))
parser.add_argument('filename', type=str, nargs=1, help='path to your `.quiz` file')

# watch input file for changes - if any detected regenerate JSON file
def regenerate(quizFilename, quizMd5):
  print("Regenerating: " + quizFilename)
  while True:
    # calculate current checksum
    currentQuizMd5 = hashlib.md5(open(quizFilename).read()).hexdigest()
    if currentQuizMd5 != quizMd5:
      print(quizFilename + " has changed, regenerating...")
      quizMd5 = currentQuizMd5
      toJson(quizFilename)
    time.sleep(5)

# runs http server for development
def serve(quizFilename, serverPort):
  # find serving directory
  serverDirPrefix = ''
  serverDir = None
  serverDir_i = quizFilename[::-1].find('/')
  if serverDir_i != -1:
    serverDir = quizFilename[::-1][serverDir_i:][::-1]
  else:
    serverDir = "./"
  # serve
  # Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
  class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def translate_path(self, path):
      if self.path.startswith(serverDirPrefix):
        if self.path == serverDirPrefix or self.path == serverDirPrefix + '/':
          return serverDir + '/index.html'
        else:
          return serverDir + path[len(serverDirPrefix):]
      else:
        return SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(self, path)
  httpd = SocketServer.TCPServer(("", serverPort), MyRequestHandler)
  print("Serving at port: " + str(serverPort))
  print("The home directory is: " + serverDir)
  httpd.serve_forever()

if __name__ == '__main__':
  # parse arguments
  args = parser.parse_args()
  serverPort = args.port
  quizFilename = args.filename[0]

  # check whether given file exist and compute its initial checksum
  quizMd5 = None
  if os.path.exists(quizFilename):
    if os.path.isfile(quizFilename):
      # .quiz extension necessary
      if quizFilename[-5:] != ".quiz":
        print("Your file must have `.quiz` extension")
        sys.exit(1)
      quizMd5 = hashlib.md5(open(quizFilename).read()).hexdigest()
    else:
      print(quizFilename + " is not a file!")
      sys.exit(1)
  else:
    print(quizFilename + " does not exist!")
    sys.exit(1)

  # generate index.html for given json <- quiz file
  indexDir_i = quizFilename[::-1].find('/')
  if indexDir_i != -1:
    indexDir = quizFilename[::-1][indexDir_i:][::-1]
  else:
    indexDir = "./"
  indexFilename = indexDir + "index.html"
  print("updating " + indexFilename)
  quizJson = quizFilename[:-5] + ".json"
  updateIndex(indexDir, quizJson)

  p1 = Process(target=regenerate, args=(quizFilename, quizMd5))
  p1.start()
  p2 = Process(target=serve, args=(quizFilename, serverPort))
  p2.start()
  raw_input("Press Enter to exit...\n")
  print("exiting...")
  p1.terminate()
  p2.terminate()
  sys.exit(0)
