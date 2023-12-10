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

# holds the missing lines for each source code
class SourceCode:
    fname = ""
    missing_lines = set()

    def __init__(self, line):
        self.parse_missed_lines(line)

    # based on https://github.com/bendrissou/gcovr-diff 'get_file_missed_lines' function
    def parse_missed_lines(self, line):
        line_data = line.split()
        self.fname = line_data[0]
        self.missing_lines = set()

        # In case there are no missed lines reported
        if len(line_data) < 5: 
            return
        
        missed_lines = line_data[-1]
        missed_lines = missed_lines.split(',')
        
        # break intervals into lists: 1-3 -> 1,2,3
        for i in range(0, len(missed_lines)):
            try:
                self.missing_lines.add(int(missed_lines[i]))
            except ValueError as ve:
                r = missed_lines[i].split('-')
                r = [int(j) for j in r]
                k=r[0]
                while (k<=r[1]):
                    self.missing_lines.add(k)
                    k+=1

    def __str__(self):
        return f"{self.fname}: {self.missing_lines}"

class Test:
    # list of type SourceCode
    list_source_files = []
    # when empty, means the entire test set
    test_name = ""
    # '-' means a negated filter
    test_filter = ""

    def __init__(self, fname, tname="", tfilter=""):
        self.test_name = tname
        self.test_filter = tfilter
        self.list_source_files = []
        with open(fname) as f:
            lines = f.read().splitlines()
        # remove the 6 initial lines and the 3 last lines.
        # we just want the list of source codes
        lines = lines[6:-3]
        #print (lines)
        for l in lines:
            code = SourceCode(l)
            #print (code)
            self.list_source_files.append(code)
    
    def __str__(self):
        line = self.test_name+self.test_filter+'\n'
        for l in self.list_source_files:
            line += " -"+str(l)+'\n'
        return line

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
    if not args.quiet:
        print (test_list)

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
        

    #4) parse the gcovr txt reports of the complete test set
    complete_report_fname = os.path.join(args.report_dir, test_exec+".txt")
    if not os.path.isfile(complete_report_fname):
        print ("ERROR: Test report", complete_report_fname, "not found")
        sys.exit(1)
    base_fname = os.path.basename(complete_report_fname)
    test_name = base_fname[:base_fname.rfind('.')]
    complete_test_missed_lines = Test(complete_report_fname, test_name)
    print(complete_test_missed_lines)

    #5) parse the gcovr txt reports to gather the missed lines for every test
    report_folder = os.path.join(args.report_dir, "*.txt")
    report_fnames = glob.glob(report_folder)
    report_fnames.remove(complete_report_fname)
    report_fnames.sort()

    list_missed_lines_tests = []
    for report_fname in report_fnames:
        # extract the test name and filter mode form the filename
        base_fname = os.path.basename(report_fname)
        test_name = base_fname[:base_fname.rfind('.')]
        test_filter = ""
        if test_name[-1] == '-':
            test_filter = "-"
            test_name = test_name[:-1]
        missed_lines = Test(report_fname, test_name, test_filter)
        print(missed_lines)
        list_missed_lines_tests.append(missed_lines)
    sys.exit(1)

    #6) do the difference between the 'full test' and each test in the test list

    #7) sort the result by the test w least number of missed lines, i.e., the tests that least contribute to the full code coverage

    #8) produce the report


if __name__ == '__main__': 
    main()
