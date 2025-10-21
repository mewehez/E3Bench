# Get a list of all .cpp files in the current directory
set(POWER_UTILS "${CMAKE_CURRENT_SOURCE_DIR}/../power_utils.cpp")

add_executable(vdd_cpu_gpu_cv main.cpp vdd_cpu_gpu_cv.cpp ${POWER_UTILS})

# Install programs
install(TARGETS vdd_cpu_gpu_cv DESTINATION bin)
