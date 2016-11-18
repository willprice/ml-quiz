#!/usr/bin/env bash
YAML_TO_JSON=./yaml2json.py

QUIZ_YAML_SRC="${1:-ml.yaml}"
QUIZ_JSON_SRC="${QUIZ_YAML_SRC%%.yaml}.quiz"

[ -f "$QUIZ_YAML_SRC" ] || {
    echo "$QUIZ_YAML_SRC doesn't exist!"
    exit 1
}

"$YAML_TO_JSON" < "$QUIZ_YAML_SRC" > "$QUIZ_JSON_SRC" || exit 2
./resources/compile_quiz.py --comments \
                            --hints \
                            --workings \
                            --explanation \
                            --count \
                            "${QUIZ_JSON_SRC}" || exit 3
rm "$QUIZ_JSON_SRC"
exit 0
