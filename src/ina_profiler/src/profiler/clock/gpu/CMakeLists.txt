# Get a list of all .cpp files in the current directory
set(CLOCK_UTILS "${CMAKE_CURRENT_SOURCE_DIR}/../clock_utils.cpp")

add_executable(get_gpu_avail_freqs get_gpu_avail_freqs.cpp)
add_executable(get_gpu_cur_freq get_gpu_cur_freq.cpp)

add_executable(set_gpu_cur_freq set_gpu_cur_freq.cpp ${CLOCK_UTILS})
add_executable(set_gpu_min_freq set_gpu_min_freq.cpp ${CLOCK_UTILS})
add_executable(set_gpu_max_freq set_gpu_max_freq.cpp ${CLOCK_UTILS})

# Install programs
install(TARGETS get_gpu_avail_freqs get_gpu_cur_freq set_gpu_cur_freq set_gpu_min_freq set_gpu_max_freq DESTINATION bin)
