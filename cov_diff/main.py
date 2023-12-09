"""
Copyright 2023 Alexandre Amory
"""

import re
import glob
import subprocess
import os
import sys
import argparse
import shutil

#1) returns a list of tests of the gtest executable
# Example:
# $> ./greatest_test --gtest_list_tests | awk '/\./{ SUITE=$1 }  /  / { print SUITE $1 }'
# GreaterTest.AisGreater
# GreaterTest.AisGreaterRedundant
# GreaterTest.BisGreater
# GreaterTest.CisGreater
def generate_gtest_list(test_exec):
    cmd=test_exec + " --gtest_list_tests | awk '/\./{ SUITE=$1 }  /  / { print SUITE $1 }'"
    result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    output = result.decode("utf-8",'ignore')
    all_tests_list = output.split('\n')
    del all_tests_list[-1]

    return all_tests_list

# run the test to generate .gcda file w coverage data and then run gcovr to generate the coverage report in txt format
# when test_exclude is not empty, it excludes the test, otherwise, it runs all tests
# it assumes the current folder is the build folder
def run_gcovr(test_exec, test_exclude):
    #TODO check if this is the build folder
    print ("Running test", test_exec, test_exclude)
    if test_exclude:
        cmd = test_exec
    else:
        cmd = test_exec + " --gtest_filter='-" + test_exclude + "'"
    result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    # TODO check for errors
    cmd = "make coverage_txt"
    result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    # TODO check for errors
    if not os.path.isfile("./coverage_txt/coverage.txt"):
        print ("ERROR: ./coverage_txt/coverage.txt not generated for:", test_exec, test_exclude)
        sys.exit(1)
    # move the coverage report to avoid being overwritten
    os.makedirs(os.path.dirname("../cov_reports/"), exist_ok=True)
    if test_exclude:
        shutil.move("./coverage_txt/coverage.txt", "../cov_reports/"+test_exec+".txt")
    else:
        shutil.move("./coverage_txt/coverage.txt", "../cov_reports/"+test_exclude+".txt")
    print ("Test", test_exec, test_exclude, "executed!")


def main():
    parser = argparse.ArgumentParser(description='Shows the number of lines each test is contributing, compared to the entire test set.')
    parser.add_argument('--test-app', type=str, required=True, help='GTest executable')
    parser.add_argument('--summary', action='store_true', help='Report summary (optional).')

    args = parser.parse_args()

    # Access the parsed arguments
    test_exec = args.test_app
    summary = args.summary


    #1) generate list of tests
    test_list = generate_gtest_list(test_exec)
    print (test_list)
    print (type(test_list))

    #2) run the full test to get it's missed lines
    # save the report in gcovr txt format w the name <test_executable>.txt
    run_gcovr(test_exec, "")

    #3) iterate on each test, excluding the test from the execution 
    # save the report in gcovr txt format w the name <test_name>.txt
    for test in test_list:
        run_gcovr(test_exec, test)

    #4) parse the gcovr txt reports to gather the missed lines for every test

    #5) do the difference between the 'full test' and each test in the test list

    #6) sort the result by the test w least number of missed lines, i.e., the tests that least contribute to the full code coverage

    #7) produce the report


if __name__ == '__main__': 
    main()
