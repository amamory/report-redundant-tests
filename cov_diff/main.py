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
    # https://stackoverflow.com/questions/24849998/how-to-catch-exception-output-from-python-subprocess-check-output
    cmd=test_exec + " --gtest_list_tests | awk '/\./{ SUITE=$1 }  /  / { print SUITE $1 }'"
    result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    output = result.decode("utf-8",'ignore')
    all_tests_list = output.split('\n')
    del all_tests_list[-1]

    return all_tests_list

# run the test to generate .gcda file w coverage data and then run gcovr to generate the coverage report in txt format
# when 'test_name' is not empty, it excludes the test, otherwise, it runs all tests
# 'test_filter_mode' is either '-' or ''. The former means a inverted filter, i.e., all tests except for 'test_name'
# it assumes the current folder is the build folder
def run_gcovr(test_exec, test_name, test_filter_mode, args):

    print ("Running test", test_exec, test_name)
    if not os.path.isfile(test_exec):
        print ("ERROR: Test executable", test_exec, "not found")
        sys.exit(1)
        
    # empty test_name means it's running the entire test set
    if test_name:
        cmd = test_exec + " --gtest_filter='"+ test_filter_mode + test_name + "'"
    else:
        cmd = test_exec
    result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    if not args.quiet:
        print( result.decode("utf-8",'ignore') )
    # TODO check for errors
    cmd = "make coverage_txt"
    # the 1st filter mode means all tests except for test_name
    # the 2nd filter mode means only test_name
    result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    if not os.path.isfile("./coverage_txt/coverage.txt"):
        print ("ERROR: ./coverage_txt/coverage.txt not generated for:", test_exec, test_name)
        sys.exit(1)
    # TODO check for errors

    if not args.quiet:
        print( result.decode("utf-8",'ignore') )
        with open('./coverage_txt/coverage.txt') as f:
            content = f.read()
            print (content)
    # move the coverage report to avoid being overwritten
    if test_name:
        dst_file = os.path.join(args.report_dir, test_name+test_filter_mode+".txt")
    else:
        dst_file = os.path.join(args.report_dir, test_exec+".txt")
    # if os.path.exists(dst_file):
    #     os.remove(dst_file)
    shutil.move("./coverage_txt/coverage.txt", dst_file)
    print ("Test", test_exec, test_name+test_filter_mode, "executed!")


def main():
    parser = argparse.ArgumentParser(description='Shows the number of lines each test is contributing, compared to the entire test set.')
    parser.add_argument('--test-app', type=str, required=True, help='GTest executable')
    parser.add_argument('--exec-dir', type=str, required=True, help='Directory where the tests must be launched')
    parser.add_argument('--report-dir', type=str, default="../cov_reports", help='Directory where the coverage reports are saved')
    parser.add_argument('--skip-tests', action='store_true', help='Skip the test execution, assuming the reports were already generated (optional).')
    parser.add_argument('--find-subset-tests', action='store_true', help='Additional check to find tests that are a subset of other tests (optional).')
    parser.add_argument('--quiet', action='store_true', help='Reduce verbosity (optional).')
    parser.add_argument('--summary', action='store_true', help='Report summary (optional).')

    args = parser.parse_args()

    try:
        os.chdir(args.exec_dir)
    except FileNotFoundError:
        print(args.exec_dir + ' does NOT exist. Aborting')
        sys.exit(1)

    os.makedirs(os.path.dirname(args.report_dir), exist_ok=True)

    # Access the parsed arguments
    test_exec = args.test_app
    summary = args.summary


    #1) generate list of tests
    test_list = generate_gtest_list(test_exec)
    print (test_list)
    print (type(test_list))

    if not args.skip_tests:
        #2) run the full test to get it's missed lines
        # save the report in gcovr txt format w the name <test_executable>.txt
        run_gcovr(test_exec, "", "", args)

        #3) iterate on each test, excluding the test from the execution 
        # save the report in gcovr txt format w the name <test_name><filter_mode>.txt
        filter_modes = ['-']
        if args.find_subset_tests:
            filter_modes.append('')
        for test in test_list:
            for fmode in filter_modes:
                run_gcovr(test_exec, test, fmode, args)
        sys.exit(1)

    #4) parse the gcovr txt reports to gather the missed lines for every test

    #5) do the difference between the 'full test' and each test in the test list

    #6) sort the result by the test w least number of missed lines, i.e., the tests that least contribute to the full code coverage

    #7) produce the report


if __name__ == '__main__': 
    main()
