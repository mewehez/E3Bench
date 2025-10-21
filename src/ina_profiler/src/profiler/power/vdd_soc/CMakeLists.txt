# Get a list of all .cpp files in the current directory
set(POWER_UTILS "${CMAKE_CURRENT_SOURCE_DIR}/../power_utils.cpp")

add_executable(vdd_soc main.cpp vdd_soc.cpp ${POWER_UTILS})

# Install programs
install(TARGETS vdd_soc DESTINATION bin)
