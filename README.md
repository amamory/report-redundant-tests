# report-redundant-tests

It reports the tests that are not contributing to the code coverage. It uses gtest, cmake, and gcovr.

## The problem 

The main problem is related to **test maintainability for legacy projects**. Let's say we two categories of tests: the old tests and the new tests. The old tests were those made in the early begginning of the project that in general have a much more limited scope compared to the newer tests.

As a consequence, the tests age, i.e., they get older. The old tests might have been supperseed by the new ones, meaning the old ones 'test less' than the new ones. Moreover, the old tests might become a hurdle to maintain, without being sure if they are still contributing to the overall test coverage. The problem is that when there are hundreds of tests, it might get complex to identify the tests that became obsolete.

## Proposed solution

This tool runs all tests, saves their uncovered lines. This is the reference coverage. Next, it runs the test again, but every time excluding one test. If the uncovered lines are the same as the reference coverage, it means this test might have become obsolete. Probably there are other tests that cover the same lines. The same process is repeated for every test. In the end, it shows a table with the test name, and the number of lines covered exclusively by it.

## Requirements

```
```


## Usage

### 1st Step: Build and run the tests

```
mkdir build; cd build
cmake ..
make -j4
make coverage_html
firefox 
```

### 2nd Step: Running the report

This process takes time, depeding on the number of tests. 

```
python3 cov_diff/main.py
```

