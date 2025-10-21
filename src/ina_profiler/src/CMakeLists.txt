# Get all .h files recursively in the current directory and subdirectories
file(GLOB_RECURSE HEADER_FILES "*.h")

# Copy each header file to PROJECT_INCLUDE_DIR without directory structure
foreach(HEADER_FILE ${HEADER_FILES})
    # Extract the filename (not the directory path)
    get_filename_component(FILE_NAME ${HEADER_FILE} NAME)
    
    # Copy the file to the target directory
    configure_file(${HEADER_FILE} "${PROJECT_INCLUDE_DIR}/${FILE_NAME}" COPYONLY)
endforeach()

add_subdirectory("profiler")
