#!/usr/bin/env python

import os
import subprocess as sp
from multiprocessing import Pool
from functools import partial
import shutil

def run_codeml(directories, c=16):
	[shutil.copy("codeml", directory) for directory in directories]
	partial_subprocess = partial(sp.call, shell=True)
	calls = ["cd {}; chmod +x codeml; ./codeml *.ctl;".format(directory) for directory in directories]
	pool = Pool(c)
	return pool.map(partial_subprocess, calls)