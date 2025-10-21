# Get a list of all .cpp files in the current directory
# file(GLOB SOURCES "*.cpp")

set(CLOCK_UTILS "${CMAKE_CURRENT_SOURCE_DIR}/../clock_utils.cpp")

add_executable(get_emc_avail_freqs get_emc_avail_freqs.cpp)
add_executable(get_emc_cur_freq get_emc_cur_freq.cpp)

add_executable(set_emc_cur_freq set_emc_cur_freq.cpp ${CLOCK_UTILS})
add_executable(set_emc_min_freq set_emc_min_freq.cpp ${CLOCK_UTILS})
add_executable(set_emc_max_freq set_emc_max_freq.cpp ${CLOCK_UTILS})

# Install programs
install(TARGETS get_emc_avail_freqs get_emc_cur_freq set_emc_cur_freq set_emc_min_freq set_emc_max_freq DESTINATION bin)
