#!/usr/bin/env python
#coding=utf-8

# Generates a config for all existing books

import os
import shutil

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def get_immediate_subdirectories(dir):
	return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

languages = get_immediate_subdirectories('../../../101results/repos/101integrate/data/languages')
themes = get_immediate_subdirectories('../../../101results/repos/101integrate/data/themes')


baseResources = '../../../101web/data/resources/'
for lang in languages:
	copytree('../../../101results/repos/101integrate/data/languages/' + lang.strip() + "/", baseResources + 'languages/' + lang.strip() + "/")

for theme in themes:
	copytree('../../../101results/repos/101integrate/data/themes/' + theme.strip() + "/", baseResources + 'themes/' + theme.strip() + "/")
