#!/usr/bin/env python2
import sys
import yaml
import json
import os


def yaml_include(loader, node):
    yaml_top_level_dir = os.path.dirname(loader.name)
    include_relative_path = node.value
    include_path = os.path.join(yaml_top_level_dir, include_relative_path)

    with file(include_path) as f:
        return yaml.load(f)


yaml.add_constructor("!include", yaml_include)

json.dump(yaml.load(sys.stdin), sys.stdout, indent=4)
