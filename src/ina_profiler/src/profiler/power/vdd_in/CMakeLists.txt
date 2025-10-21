# Get a list of all .cpp files in the current directory
set(POWER_UTILS "${CMAKE_CURRENT_SOURCE_DIR}/../power_utils.cpp")

add_executable(vdd_in main.cpp vdd_in.cpp ${POWER_UTILS})

# Install programs
install(TARGETS vdd_in DESTINATION bin)
