# Dictionary with mlbook chapters and sections
questionCategories = {\
  1:\
    {\
    0:"The ingredients of machine learning",
    1:"Tasks: the problems that can be solved with machine learning",
    2:"Models: the output of machine learning",
    3:"Features: the workhorses of machine learning"
    },
  2:\
    {\
    0:"Binary classification and related tasks",
    1:"Classification",
    2:"Scoring and ranking",
    3:"Class probability estimation"
    },
  3:
    {\
    0:"Beyond binary classification",
    1:"Handling more than two classes",
    2:"Regression",
    3:"Unsupervised and descriptive learning"
    },
  4:\
    {\
    0:"Concept learning",
    1:"The hypothesis space",
    2:"Paths through the hypothesis space",
    3:"Beyond conjunctive concepts",
    4:"Learnability"
    },
  5:\
    {\
    0:"Tree models",
    1:"Decision trees",
    2:"Ranking and probability estimation trees",
    3:"Tree learning as variance reduction"
    },
  6:\
    {\
    0:"Rule models",
    1:"Learning ordered rule lists",
    2:"Learning unordered rule sets",
    3:"Descriptive rule learning",
    4:"First-order rule learning"
    },
  7:\
    {\
    0:"Linear models",
    1:"The least-squares method",
    2:"The perceptron",
    3:"Support vector machines",
    4:"Obtaining probabilities from linear classifiers",
    5:"Going beyond linearity with kernel methods"
    },
  8:\
    {\
    0:"Distance-based models",
    1:"So many roads...",
    2:"Neighbours and exemplars",
    3:"Nearest-neighbour classification",
    4:"Distance-based clustering",
    5:"Hierarchical clustering",
    6:"From kernels to distances"
    },
  9:\
    {\
    0:"Probabilistic models",
    1:"The normal distribution and its geometric interpretations",
    2:"Probabilistic models for categorical data",
    3:"Discriminative learning by optimising conditional likelihood",
    4:"Probabilistic models with hidden variables",
    5:"Compression-based models"
    },
  10:\
    {\
    0:"Features",
    1:"Kinds of feature",
    2:"Feature transformations",
    3:"Feature construction and selection"
    },
  11:\
    {\
    0:"Model ensembles",
    1:"Bagging and random forests",
    2:"Boosting",
    3:"Mapping the ensemble landscape"
    },
  12:\
    {\
    0:"Machine learning experiments",
    1:"What to measure",
    2:"How to measure it",
    3:"How to interpret it"
    }\
}

iframeGeneralTemplate = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">
<html>
   <head>
     <title>One-by-one quiz</title>
   </head>
   <body>

%(iframes)s

   </body>
</html>

"""

iframeIframeTemplate = """

<iframe
 src="%(filename)s"
 width="100%%" height="600"
>
  <p>
    <a href="%(filename)s">
      Fallback link for browsers that, unlikely, don't support frames
    </a>
  </p>
</iframe>

"""

questionTemplate = """

<!-- START OF QUESTION %(questionNumber)d -->

<li class="wpProQuiz_listItem" style="display: none;">
  <h5 style="display: inline-block;" class="wpProQuiz_header"><span>%(questionNumber)d</span>. Question</h5>
  <div style="font-weight: bold; padding-top: 5px;">Category: %(category)s</div>
  <div style="font-weight: bold; padding-top: 5px;">Category: %(difficulty)s</div>

  <!-- QUESTION (SINGLE ANSWER) -->
  <div class="wpProQuiz_question" style="margin: 10px 0px 0px 0px;">

    <!-- QUESTION -->
    <div class="wpProQuiz_question_text"><p>%(question)s</p></div>

    <!-- ANSWER -->
    <ul class="wpProQuiz_questionList" data-question_id="%(id)d" data-type="%(answerType)s">%(answersStr)s</ul>
  </div>


  <input type="button" name="back" value="Back" class="wpProQuiz_button wpProQuiz_QuestionButton" style="float: left !important; margin-right: 10px !important; display: none;">
  <input type="button" name="next" value="Next" class="wpProQuiz_button wpProQuiz_QuestionButton" style="float: right; display: none;">
  <div style="clear: both;"></div>
</li>

<!-- END OF QUESTION %(questionNumber)d -->

"""

quizTemplate = """<!doctype html>
<!--[if !IE]>
<html class="no-js non-ie" lang="en-US">

<![endif]-->
<!--[if IE 7 ]>
<html class="no-js ie7" lang="en-US">

<![endif]-->
<!--[if IE 8 ]>
<html class="no-js ie8" lang="en-US">

<![endif]-->
<!--[if IE 9 ]>
<html class="no-js ie9" lang="en-US">

<![endif]-->
<!--[if gt IE 9]>
<!-->
<html class="no-js" lang="en-US">
  <!--
<![endif]-->
  <head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
      Machine Learning &#124; Quizzes
    </title>
    <link rel="profile" href="http://gmpg.org/xfn/11"/>
    <link rel="pingback" href="http://python.otuama.net/xmlrpc.php"/>
    <link rel="alternate" type="application/rss+xml" title="Machine Learning &raquo; Feed" href="http://python.otuama.net/feed/"/>
    <link rel="alternate" type="application/rss+xml" title="Machine Learning &raquo; Comments Feed" href="http://python.otuama.net/comments/feed/"/>
    <link rel='stylesheet' id='wpProQuiz_front_style-css' href='resources/css/wpProQuiz_front.min.css?ver=0.28' type='text/css' media='all'/>
    <link rel='stylesheet' id='responsive-style-css' href='resources/css/responsive_style.css?ver=1.9.3.4' type='text/css' media='all'/>
    <link rel='stylesheet' id='responsive-media-queries-css' href='resources/css/responsive_core_style.css?ver=1.9.3.4' type='text/css' media='all'/>
    <script type='text/javascript' src='resources/js/wp_jquery.js?ver=1.10.2'>
    </script>
    <script type='text/javascript' src='resources/js/wp_jquery-migrate.min.js?ver=1.2.1'>
    </script>
    <script type='text/javascript' src='resources/js/responsive_core_responsive-modernizr.js?ver=2.6.1'>
    </script>
    <link rel="EditURI" type="application/rsd+xml" title="RSD" href="http://python.otuama.net/xmlrpc.php?rsd"/>
    <link rel="wlwmanifest" type="application/wlwmanifest+xml" href="http://python.otuama.net/wp-includes/wlwmanifest.xml"/>
    <meta name="generator" content="WordPress 3.6.1"/>
    <!-- We need this for debugging -->
    <!-- Responsive 1.9.3.8 -->
    <script type="text/x-mathjax-config">
      MathJax.Hub.Config({
        tex2jax: {
          inlineMath: [['$','$']],
          displayMath: [ ['$$','$$'] ]
        }
      });
    </script>
    <script
    type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">

    </script>
  </head>
  <body class="home blog">
    <div id="container" class="hfeed">
      <div id="header">
    <div id="logo">

      </div>
      <!-- end of #logo -->
  </div>
  <!-- end of #header -->
  <div id="wrapper" class="clearfix">
    <div id="content-blog" class="grid col-940">
      <!-- Blog page title -->
      <h1>
      </h1>
      <div id="post-10" class="post-10 post type-post status-publish format-standard hentry category-distance-models category-quiz">
        <h2 class="entry-title post-title">
          <a href="#" rel="bookmark">
            Machine Learning Quiz
          </a>
        </h2>


        <!-- end of .post-meta -->
        <div class="post-entry">
          <div class="wpProQuiz_content" id="wpProQuiz_2">
            <h2>%(quizTitle)s</h2>




          <div style="display: none;" class="wpProQuiz_results">
            <h4 class="wpProQuiz_header">
              Results
            </h4>
            <p class="wpProQuiz_time_limit_expired" style="display: none;">
              Time has elapsed
            </p>
            <div class="wpProQuiz_catOverview" style="display:none;">
              <h4>
                Categories
              </h4>
              <div style="margin-top: 10px;">
                <ol>
                  <li data-category_id="0">
                    <span class="wpProQuiz_catName">
                      Not categorized
                    </span>
                    <span class="wpProQuiz_catPercent">
                    </span>
                  </li>
                  <li data-category_id="4">
                    <span class="wpProQuiz_catName">
                      Distance
                    </span>
                    <span class="wpProQuiz_catPercent">
                    </span>
                  </li>
                </ol>
              </div>
            </div>
            <div>
              <ul class="wpProQuiz_resultsList">
                <li style="display: none;">
                  <div>
                  </div>
                </li>
              </ul>
            </div>
            <div style="margin: 10px 0px;">
              <input class="wpProQuiz_button" type="button" name="restartQuiz" value="Restart quiz">
              <input class="wpProQuiz_button" type="button" name="reShowQuestion" value="View questions">
            </div>
          </div>

          <div class="wpProQuiz_quizAnker" style="display: none;">
          </div>
          <div style="display: none;" class="wpProQuiz_quiz">
            <ol class="wpProQuiz_list">%(questions)s</ol>
          </div>
        </div>
        <script type="text/javascript">
          jQuery(document).ready(function($) {
      $('#wpProQuiz_2').wpProQuizFront({
              quizId: 2,
              mode: 1,
              globalPoints: 8,
              timelimit: 0,
              resultsGrade: [0],
              bo: 1031,
              qpp: 0,
              catPoints: {"4":1,"0":7}
              ,
              formPos: 0,
              lbn: "Finish quiz",
              json: %(answersJSON)s      }
                                            );
          }
                                );
    </script>
      </div>
      <!-- end of .post-entry -->
      <!-- end of .post-data -->
      <div class="post-edit">
      </div>
    </div>
    <!-- end of #post-10 -->
  </div>
  <!-- end of #content-blog -->
  </div>
  <!-- end of #wrapper -->
  </div>
  <!-- end of #container -->

  <script type='text/javascript' src='http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'>
  </script>
  <!-- MathJax Latex Plugin installed -->
  <script type='text/javascript' src='resources/js/responsive_core_responsive-scripts.js?ver=1.2.4'>
  </script>
  <script type='text/javascript' src='resources/js/wp_ui_jquery_core.min.js?ver=1.10.3'>
  </script>
  <script type='text/javascript' src='resources/js/wp_ui_jquery_widget.min.js?ver=1.10.3'>
  </script>
  <script type='text/javascript' src='resources/js/wp_ui_jquery_mouse.min.js?ver=1.10.3'>
  </script>
  <script type='text/javascript' src='resources/js/wp_ui_jquery_sortable.min.js?ver=1.10.3'>
  </script>
  <script type='text/javascript'>
    /* <![CDATA[ */
    var WpProQuizGlobal = {"ajaxurl":"resources\/php\/wp_admin-ajax.php","loadData":"Loading","questionNotSolved":"You must answer this question.","questionsNotSolved":"You must answer all questions before you can completed the quiz.","fieldsNotFilled":"All fields have to be filled."}
        ;
    /* ]]> */
  </script>
  <script type='text/javascript' src='resources/js/wpProQuiz_front.min.js?ver=0.28'>
  </script>
  <script type='text/javascript' src='resources/js/wpProQuiz_jquery.ui.touch-punch.min.js?ver=0.2.2'>
  </script>
</body>
</html>"""

blankItem = \
"""
<span class="wpProQuiz_cloze">
  <input data-wordlen="%(length)d" type="text" value="">
  <span class="wpProQuiz_clozeCorrect" style="display: none;">%(answers)s</span>
</span>
"""

blankTemplate = \
"""
<li class="wpProQuiz_questionListItem" data-pos="0">%s</li>
"""

tableTemplate = \
"""
<li class="wpProQuiz_questionListItem" data-pos="0">
<table>
  <tbody>
  <tr><td></td><td>Predicted+</td><td>Predicted-</td><td></td></tr>
  <tr>
    <td>Actual+</td>
    <td><span class="wpProQuiz_cloze">%s<input data-wordlen="2" type="text" value=""><span class="wpProQuiz_clozeCorrect" style="display: none;">(%s)</span></span></td>
    <td><span class="wpProQuiz_cloze">%s<input data-wordlen="2" type="text" value=""><span class="wpProQuiz_clozeCorrect" style="display: none;">(%s)</span></span></td>
    <td><span class="wpProQuiz_cloze">%s<input data-wordlen="2" type="text" value=""><span class="wpProQuiz_clozeCorrect" style="display: none;">(%s)</span></span></td>
  </tr>
  <tr>
    <td>Actual-</td>
    <td><span class="wpProQuiz_cloze">%s<input data-wordlen="2" type="text" value=""><span class="wpProQuiz_clozeCorrect" style="display: none;">(%s)</span></span></td>
    <td><span class="wpProQuiz_cloze">%s<input data-wordlen="2" type="text" value=""><span class="wpProQuiz_clozeCorrect" style="display: none;">(%s)</span></span></td>
    <td><span class="wpProQuiz_cloze">%s<input data-wordlen="2" type="text" value=""><span class="wpProQuiz_clozeCorrect" style="display: none;">(%s)</span></span></td>
  </tr>
  <tr>
    <td></td>
    <td><span class="wpProQuiz_cloze">%s<input data-wordlen="2" type="text" value=""><span class="wpProQuiz_clozeCorrect" style="display: none;">(%s)</span></span></td>
    <td><span class="wpProQuiz_cloze">%s<input data-wordlen="2" type="text" value=""><span class="wpProQuiz_clozeCorrect" style="display: none;">(%s)</span></span></td>
    <td><span class="wpProQuiz_cloze">%s<input data-wordlen="3" type="text" value=""><span class="wpProQuiz_clozeCorrect" style="display: none;">(%s)</span></span></td>
  </tr>
  </tbody>
</table>
</li>
"""

singleTemplate = \
"""
<li class="wpProQuiz_questionListItem" data-pos="%(answerPos_0)d">
<span style="display:none;"></span>
<label><input class="wpProQuiz_questionInput" type="radio" name="question_2_%(id)d" value="%(answerPos_1)d">%(answerText)s</label>
</li>
"""

sortTemplate = \
"""
<li class="wpProQuiz_questionListItem" data-pos="%(answerPos_0)d"><div class="wpProQuiz_sortable">%(answerText)s</div></li>
"""

multipleTemplate = \
"""
<li class="wpProQuiz_questionListItem" data-pos="%(answerPos_0)d">
<span style="display:none;">
</span>
<label>
<input class="wpProQuiz_questionInput" type="checkbox" name="question_2_%(id)d" value="%(answerPos_1)d">
%(answerText)s
</label>
</li>
"""

"""
Due to the internal code structure of the quiz code, this matrix sort question type requires
multiple templates to be defined. This class also does not use the same question template
that other question types use.
"""

matrixSort_answers_single = \
r"""
<li class="wpProQuiz_sortStringItem" data-pos="%(answerPos_0)d" data-correct="%(answerPos_0)d">%(answer)s</li>
"""

matrixSort_question_single = \
r"""
<li class="wpProQuiz_questionListItem" data-pos="%(answerPos_0)d"><table><tbody><tr class="wpProQuiz_mextrixTr"><td width="20%%"><div class="wpProQuiz_maxtrixSortText">%(answer)s</div></td><td width="80%%"><ul class="wpProQuiz_maxtrixSortCriterion"></ul></td></tr></tbody></table></li>
"""

matrixSort_questionTemplate = \
"""

<!-- START OF QUESTION %(questionNumber)d -->

<li class="wpProQuiz_listItem" style="display: none;">
  <!-- <div class="wpProQuiz_question_page"> <span>%(questionNumber)d</span> of <span>%(numQuestions)d</span></div> -->
  <h5 style="display: inline-block;" class="wpProQuiz_header"><span>%(questionNumber)d</span>. Question</h5>
  <div style="font-weight: bold; padding-top: 5px;">Category: %(category)s</div>
  <div style="font-weight: bold; padding-top: 5px;">Category: %(difficulty)s</div>

  <div class="wpProQuiz_question" style="margin: 10px 0px 0px 0px;">
    <div class="wpProQuiz_question_text"><p>%(question)s</p></div>

    <div class="wpProQuiz_matrixSortString">
      <h5 class="wpProQuiz_header">Sort elements</h5>
      <ul class="wpProQuiz_sortStringList">%(ms_questions)s</ul>
      <div style="clear: both;"></div>
    </div>

    <ul class="wpProQuiz_questionList" data-question_id="16" data-type="matrix_sort_answer">%(ms_answers)s</ul>
  </div>

  <input type="button" name="back" value="Back" class="wpProQuiz_button wpProQuiz_QuestionButton" style="float: left !important; margin-right: 10px !important; display: none;">
  <input type="button" name="next" value="Next" class="wpProQuiz_button wpProQuiz_QuestionButton" style="float: right; display: none;">
  <div style="clear: both;"></div>
</li>

<!-- END OF QUESTION %(questionNumber)d -->

"""
