#ifndef __INA3221_H
#define __INA3221_H

#include <atomic>
#include <fstream>
#include <string>

#define BUFF_SIZE 100
#define PROFILER_SLEEP_MS 5

#define INA_DEVICE_VERSION "3221"
#define INA_DEVICE_PATH "/sys/bus/i2c/drivers/ina3221/1-0040/hwmon/hwmon3"

#define INA_RAIL_COUNT 3
#define INA_RAIL1_NAME "VDD_IN"
#define INA_RAIL2_NAME "VDD_CPU_GPU_CV"
#define INA_RAIL3_NAME "VDD_SOC"


// Sets/gets rail name.
#define INA_RAIL_LABEL INA_DEVICE_PATH "/" "in%d_label"

// Gets rail current in milliamperes (mA).
#define INA_CURRENT INA_DEVICE_PATH "/" "curr%d_input"

// Gets rail voltage in millivolts (mV).
#define INA_VOLTAGE INA_DEVICE_PATH "/" "in%d_input"

// Sets/gets rail instantaneous current limit in milliamperes.
#define INA_CURRENT_CRIT INA_DEVICE_PATH "/" "curr%d_crit"

// Sets/gets rail average current limit in milliamperes.
#define INA_CURRENT_MAX INA_DEVICE_PATH "/" "curr%d_max"


#endif
