from .env import create_module_env, env

import os
import sys
import traceback

class Executor(object):

    def __init__(self, module):
        self._module = module
        self._env = create_module_env(env, self._module)

    def _exec(self, change):
        try:
            self._module.run(self._env, change)
        except:
            print(
                'module_failed',
                traceback.format_exc()
            )

    def run(self, changes):
        for change in changes:
            self._exec(change)

class FileFullSweepExecutor(Executor):

    def run(self, changes):
        for root, dirs, files in os.walk(env['repo101dir']):
            for f in files:
                if '.git' in os.path.join(root, f):
                    continue

                change = {
                    'type': 'NEW_FILE',
                    'file': os.path.join(root, f).replace(env['repo101dir'] + os.sep, '')
                }

                self._exec(change)

class AllFullSweepExecutor(Executor):

    def _exec(self):
        try:
            self._module.run(self._env)
        except:
            print(
                'module_failed',
                traceback.format_exc()
            )

    def run(self, changes):
        self._exec()
