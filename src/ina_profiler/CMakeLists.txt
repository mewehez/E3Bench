cmake_minimum_required(VERSION 3.9)
message(STATUS "CMAKE version: ${CMAKE_VERSION}")

project(JETSON_PROFILER LANGUAGES CXX)

# Set C++17 as the standard for the project
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)  # Ensure C++17 is strictly enforced
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Optional: Enable C++17-related warnings or optimizations (if desired)
add_compile_options(-Wall -Wextra)  # Enable all warnings, you can modify this as needed

# Set project output directories
set(PROJECT_OUTPUT_DIR "${PROJECT_BINARY_DIR}/${CMAKE_SYSTEM_PROCESSOR}")
set(PROJECT_INCLUDE_DIR "${PROJECT_BINARY_DIR}/includes")

message(STATUS "Project include dir: ${PROJECT_INCLUDE_DIR}")
message(STATUS "Project output dir: ${PROJECT_OUTPUT_DIR}")

file(MAKE_DIRECTORY ${PROJECT_INCLUDE_DIR})
file(MAKE_DIRECTORY ${PROJECT_OUTPUT_DIR}/bin)

# Provide an option for setting the application install directory
set(APP_INSTALL_DIR "${PROJECT_OUTPUT_DIR}" CACHE PATH "The directory where the project will be installed")

# Set CMake output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${APP_INSTALL_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${APP_INSTALL_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${APP_INSTALL_DIR}/lib)

# Headers include directories
include_directories(${PROJECT_INCLUDE_DIR})

# Build subdirectories
add_subdirectory("src")
