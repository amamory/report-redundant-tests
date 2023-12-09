cmake_minimum_required(VERSION 3.16)
project(greatest)

# GoogleTest requires at least C++14
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

SET( CMAKE_BUILD_TYPE Debug )

find_package(GTest REQUIRED CONFIG)

# The unit under test
add_library(greatest_lib ./src/greatest.cpp)
add_executable(greatest ./src/main.cpp)
target_include_directories(greatest PUBLIC ./src/)
target_link_libraries(greatest greatest_lib)

# Enabling code coverage
if (CMAKE_BUILD_TYPE MATCHES Debug)
    set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
        "${CMAKE_CURRENT_SOURCE_DIR}/cmake"
    )
    include(CodeCoverage)
    #set ( CODE_COVERAGE_VERBOSE TRUE )
    append_coverage_compiler_flags()
    list(APPEND COVERAGE_EXCLUDES 
        "${CMAKE_CURRENT_SOURCE_DIR}/cmake/*"
        "${CMAKE_CURRENT_SOURCE_DIR}/test/*"
    )
    setup_target_for_coverage_gcovr_html(
        NAME coverage_html
        EXECUTABLE ctest -j3
        BASE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/src"
    )
endif()

# Unit Tests
enable_testing()
add_executable(greatest_test ./test/main_test.cpp)
target_include_directories(greatest_test PUBLIC ./src/)
target_link_libraries(greatest_test pthread gtest gtest_main greatest_lib)

include(GoogleTest)
gtest_discover_tests(greatest_test)
