# report-redundant-tests

It reports the tests that are not contributing to the code coverage. It uses gtest, cmake, and [gcovr](https://gcovr.com/en/stable/installation.html).

## The problem 

The main problem is related to **test maintainability for legacy projects**. Let's say we two categories of tests: the old tests and the new tests. The old tests were those made in the early begginning of the project that in general have a much more limited scope compared to the newer tests.

As a consequence, the tests age, i.e., they get older. The old tests might have been supperseed by the new ones, meaning the old ones 'test less' than the new ones. Moreover, the old tests might become a hurdle to maintain, without being sure if they are still contributing to the overall test coverage. The problem is that when there are hundreds of tests, it might get complex to identify the tests that became obsolete.

## Proposed solution

This tool runs all tests, saves their uncovered lines. This is the reference coverage. Next, it runs the test again, but every time excluding one test. If the uncovered lines are the same as the reference coverage, it means this test might have become obsolete. Probably there are other tests that cover the same lines. The same process is repeated for every test. In the end, it shows a table with the test name, and the number of lines covered exclusively by it.

## Requirements

Don't use `apt` to install gtest and gcovr. Please, use the following procedure: 

```
$> pip3 install env
$> python3 -m venv env
$> source env/bin/activate
$> python3 -m pip install --upgrade pip
$> python3 -m pip install --upgrade Pillow
$> pip3 install -r requirements.txt
```



## Usage

### 1st Step: Build and run the tests

```
$> mkdir build; cd build
$> cmake ..
$> make -j4
$> make coverage_html
$> firefox ./coverage_html/index.html &
```

This is the expected test result:

```bash
$> ./greatest_test
[==========] Running 4 tests from 1 test suite.
[----------] Global test environment set-up.
[----------] 4 tests from GreaterTest
[ RUN      ] GreaterTest.AisGreater
[       OK ] GreaterTest.AisGreater (0 ms)
[ RUN      ] GreaterTest.AisGreaterRedundant
[       OK ] GreaterTest.AisGreaterRedundant (0 ms)
[ RUN      ] GreaterTest.BisGreater
[       OK ] GreaterTest.BisGreater (0 ms)
[ RUN      ] GreaterTest.CisGreater
[       OK ] GreaterTest.CisGreater (0 ms)
[----------] 4 tests from GreaterTest (0 ms total)

[----------] Global test environment tear-down
[==========] 4 tests from 1 test suite ran. (0 ms total)
[  PASSED  ] 4 tests.
```

and this is the expected coverage:

```
$> make coverage_txt
$> cat ./coverage_txt/coverage.txt
------------------------------------------------------------------------------
                           GCC Code Coverage Report
Directory: ../src
------------------------------------------------------------------------------
File                                       Lines    Exec  Cover   Missing
------------------------------------------------------------------------------
greatest.cpp                                   6       6   100%
main.cpp                                       9       0     0%   6,8-10,12-14,16-17
------------------------------------------------------------------------------
TOTAL                                         15       6    40%
------------------------------------------------------------------------------
```

One of the main jobs of this script is to parse the following string `6,8-10,12-14,16-17` to identify the missed lines of each file.
s
### 2nd Step: Running the report

This process takes time, depeding on the number of tests. 

```
python3 cov_diff/main.py
```

## How it Works

### Getting the total list of tests

This is how we get the complete list of tests with gtest:

```bash
$> ./greatest_test --gtest_list_tests | awk '/\./{ SUITE=$1 }  /  / { print SUITE $1 }'
GreaterTest.AisGreater
GreaterTest.AisGreaterRedundant
GreaterTest.BisGreater
GreaterTest.CisGreater
```

### Excluding one test at a time

Next, remove one test of the test list, and repeat it until all test have been removed, one at at time. Use `--gtest_filter` with negation to indicate the test to be removed. Example:

```bash
$> ./greatest_test --verbose --gtest_filter="-GreaterTest.AisGreaterRedundant"
Note: Google Test filter = -GreaterTest.AisGreaterRedundant
[==========] Running 3 tests from 1 test suite.
[----------] Global test environment set-up.
[----------] 3 tests from GreaterTest
[ RUN      ] GreaterTest.AisGreater
[       OK ] GreaterTest.AisGreater (0 ms)
[ RUN      ] GreaterTest.BisGreater
[       OK ] GreaterTest.BisGreater (0 ms)
[ RUN      ] GreaterTest.CisGreater
[       OK ] GreaterTest.CisGreater (0 ms)
[----------] 3 tests from GreaterTest (0 ms total)

[----------] Global test environment tear-down
[==========] 3 tests from 1 test suite ran. (0 ms total)
[  PASSED  ] 3 tests.
```

# Related projects

 - https://github.com/bendrissou/gcovr-diff