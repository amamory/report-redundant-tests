"""
Copyright 2023 Alexandre Amory
"""

import re
import glob
import subprocess
import os
import sys
import argparse

#1) generate the list of tests

#2) run the full test to get it's missed lines
# save the report in gcovr txt format w the name <test_executable>.txt

#3) iterate on each test, excluding the test from the execution 
# save the report in gcovr txt format w the name <test_name>.txt

#4) parse the gcovr txt reports to gather the missed lines for every test

#5) do the difference between the 'full test' and each test in the test list

#6) sort the result by the test w least number of missed lines, i.e., the tests that least contribute to the full code coverage

#7) produce the report

