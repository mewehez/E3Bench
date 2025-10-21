#ifndef __BOARD_JON_H
#define __BOARD_JON_H

#include <fstream>

/// EMC CLOCKING ///

// Reading all Possible EMC frequencies
#define EMC_ALL_FREQS "/sys/kernel/debug/bpmp/debug/emc/tables/regular/"

// Reading EMC frequency (current and boundaries)
#define EMC_MIN_FREQ "/sys/kernel/debug/bpmp/debug/clk/emc/min_rate"
#define EMC_MAX_FREQ "/sys/kernel/debug/bpmp/debug/clk/emc/max_rate"
#define EMC_CUR_FREQ "/sys/kernel/debug/bpmp/debug/clk/emc/rate"

// Changing EMC frequency (current and boundaries)
#define MRQ_RATE_LOCK "/sys/kernel/debug/bpmp/debug/clk/emc/mrq_rate_locked"
#define EMC_STATE "/sys/kernel/debug/bpmp/debug/clk/emc/state"

/// GPU CLOCKING ///

// Reading all possible frequencies for a GPU
#define GPU_ALL_FREQS "/sys/devices/17000000.ga10b/devfreq/17000000.ga10b/available_frequencies"

// Reading GPU frequency (current and boundaries)
#define GPU_MIN_FREQ "/sys/devices/17000000.ga10b/devfreq/17000000.ga10b/min_freq"
#define GPU_MAX_FREQ "/sys/devices/17000000.ga10b/devfreq/17000000.ga10b/max_freq"
#define GPU_CUR_FREQ "/sys/devices/17000000.ga10b/devfreq/17000000.ga10b/cur_freq"

// Automated 3D Frequence Scaling (enabled by default)
#define GPU_3D_FREQ "/sys/devices/17000000.ga10b/enable_3d_scaling"



#define GPU_DVFS "/sys/devices/17000000.ga10b/devfreq/17000000.ga10b"


#define NUM_CPUS 6

// Enable/Disable CPUs
#define CPU_STATUS "/sys/devices/system/cpu/cpu%d/online"

// Reading all possible frequencies for a CPU
#define CPU_ALL_FREQS "/sys/devices/system/cpu/cpu%d/cpufreq/scaling_available_frequencies"

// Reading CPU frequency (current and boundaries)
#define CPU_MIN_FREQ "/sys/devices/system/cpu/cpu%d/cpufreq/cpuinfo_min_freq"
#define CPU_MAX_FREQ "/sys/devices/system/cpu/cpu%d/cpufreq/cpuinfo_max_freq"
#define CPU_CUR_FREQ "/sys/devices/system/cpu/cpu%d/cpufreq/cpuinfo_cur_freq"

// Changing the CPU frequency (current and boundaries)
#define SET_CPU_MIN_FREQ "/sys/devices/system/cpu/cpu%d/cpufreq/scaling_min_freq"
#define SET_CPU_MAX_FREQ "/sys/devices/system/cpu/cpu%d/cpufreq/scaling_max_freq"
// NOTE: To set the static frequency, set min and max to the same value.


// Reading GPU frequency (current and boundaries)
#define GPU_MIN_FREQ "/sys/devices/17000000.ga10b/devfreq/17000000.ga10b/min_freq"
#define GPU_MAX_FREQ "/sys/devices/17000000.ga10b/devfreq/17000000.ga10b/max_freq"
#define GPU_CUR_FREQ "/sys/devices/17000000.ga10b/devfreq/17000000.ga10b/cur_freq"

// Changing the GPU frequency (current and boundaries)
#define SET_GPU_MIN_FREQ "/sys/devices/17000000.ga10b/devfreq/17000000.ga10b/min_freq"
#define SET_GPU_MAX_FREQ "/sys/devices/17000000.ga10b/devfreq/17000000.ga10b/max_freq"
// NOTE: To set the static frequency, set min and max to the same value.






// Temperature
// TO get all termal zones
// ls -d /sys/devices/virtual/thermal/thermal_zone*
// TO get the names of thermal zone 0, for example, use 
// cat /sys/devices/virtual/thermal/thermal_zone0/type

#define ZONE0_CUR_TEMP "/sys/devices/virtual/thermal/thermal_zone0/temp" // 0 -> CPU-therm
#define ZONE1_CUR_TEMP "/sys/devices/virtual/thermal/thermal_zone1/temp" // 1 -> GPU-therm
#define ZONE2_CUR_TEMP "/sys/devices/virtual/thermal/thermal_zone2/temp" // 2 -> CV0-therm
#define ZONE3_CUR_TEMP "/sys/devices/virtual/thermal/thermal_zone3/temp" // 3 -> CV1-therm
#define ZONE4_CUR_TEMP "/sys/devices/virtual/thermal/thermal_zone4/temp" // 4 -> CV2-therm
#define ZONE5_CUR_TEMP "/sys/devices/virtual/thermal/thermal_zone5/temp" // 5 -> SOC0-therm
#define ZONE6_CUR_TEMP "/sys/devices/virtual/thermal/thermal_zone6/temp" // 6 -> SOC1-therm
#define ZONE7_CUR_TEMP "/sys/devices/virtual/thermal/thermal_zone7/temp" // 7 -> SOC2-therm
#define ZONE8_CUR_TEMP "/sys/devices/virtual/thermal/thermal_zone8/temp" // 8 -> tj-therm


#endif
