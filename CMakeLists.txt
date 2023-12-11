cmake_minimum_required(VERSION 3.16)
project(greatest)

# GoogleTest requires at least C++14
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

SET( CMAKE_BUILD_TYPE Debug )

find_package(GTest REQUIRED CONFIG)

# The unit under test
add_library(greatest_lib ./src/greatest.cpp)
add_library(cond_lib ./src/cond_cov.cpp)
add_executable(greatest ./src/main.cpp)
target_include_directories(greatest PUBLIC ./src/)
target_link_libraries(greatest greatest_lib cond_lib)

# Enabling code coverage
if (CMAKE_BUILD_TYPE MATCHES Debug)
    set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
        "${CMAKE_CURRENT_SOURCE_DIR}/cmake"
    )
    include(CodeCoverage)
    #set ( CODE_COVERAGE_VERBOSE TRUE )
    append_coverage_compiler_flags()
    # only needed to remove subfolders/files under the BASE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/src"
    list(APPEND COVERAGE_EXCLUDES 
        "${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp"
    )
    # better looking report. not the one used by the script
    setup_target_for_coverage_gcovr_html(
        NAME coverage_html
        EXECUTABLE greatest_test 
        BASE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/src"
    )
    # this is the main report format used by the script
    setup_target_for_coverage_gcovr_txt(
        NAME coverage_txt
        EXECUTABLE ;
        BASE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/src"
    )
    ## this is the rule to run when one test is excluded
    # should produce the following line in the makefile
    # /home/user/repos/dmo1mi/report-redundant-tests/build/greatest_test --gtest_filter='-$(TEST_NAME)'
    # /home/user/repos/dmo1mi/report-redundant-tests/build/greatest_test "--gtest_filter=-$${TEST_NAME}"
    # setup_target_for_coverage_gcovr_txt(
    #     NAME coverage_txt_exclude
    #     EXECUTABLE ;
    #     BASE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/src"
    # )
endif()

# Unit Tests
enable_testing()
add_executable(greatest_test ./test/main_test.cpp)
target_include_directories(greatest_test PUBLIC ./src/)
target_link_libraries(greatest_test pthread gtest gtest_main greatest_lib)

add_executable(cond_test ./test/cond_test.cpp)
target_include_directories(cond_test PUBLIC ./src/)
target_link_libraries(cond_test pthread gtest gtest_main cond_lib)

include(GoogleTest)
gtest_discover_tests(greatest_test)
gtest_discover_tests(cond_test)
