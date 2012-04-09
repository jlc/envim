# EnvimTools.py
#
# Copyright 2012 Jeanluc Chasseriau <jeanluc@lo.cx>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from VimHelpers import *
from Helper import *

log = logging.getLogger('envim')

@SimpleSingleton
class State(object):
  def __init__(self):
    self.initialized = False
    self.indexerReady = False
    self.compilerReady = False
    self.fullTypecheckFinished = False
    self.scalaNotes = []
    self.javaNotes = []

# TODO: Transform checkInitialized() and checkCompilerReady() in to decorator?
def checkInitialized():
  if not State().initialized:
    echoe("Project is not initialized. Ensure you have a .ensime project file and start using `:Envim`.")
    return False
  return True

def checkCompilerReady():
  if not checkInitialized(): return False
  if not State().compilerReady:
    echoe("Compiler is not ready yet.")
    return False
  return True

