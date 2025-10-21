#include <iostream>
#include <atomic>
#include <fstream>
#include <sstream>
#include <chrono>
#include <thread>
#include <string>
#include "ina3221.h"
#include "power_utils.h"
#include "vdd_soc.h"

extern std::atomic<bool> stopProfilerThread;


void readRail3Power(std::ofstream &output) {
    char currPath[BUFF_SIZE], voltPath[BUFF_SIZE];
    std::ifstream currFile, voltFile;
    std::ostringstream errorStream;

    // Open sensor files for each value
    sprintf(currPath, INA_CURRENT, RAIL_ID);
    sprintf(voltPath, INA_VOLTAGE, RAIL_ID);
    openFileStream(currPath, currFile, errorStream);
    openFileStream(voltPath, voltFile, errorStream);

    if (!errorStream.str().empty())
    {
        throw std::runtime_error("Error while opening files.\nCould not open the following files:\n" + errorStream.str());
    }

    std::cout << "[INFO] Opened INA files for profiling\n";
    output << "timestamp,current,voltage\n";

    auto startTime = std::chrono::duration_cast<std::chrono::nanoseconds>(
                             std::chrono::high_resolution_clock::now().time_since_epoch())
                             .count();
    auto currentTime = std::chrono::duration_cast<std::chrono::nanoseconds>(
                             std::chrono::high_resolution_clock::now().time_since_epoch())
                             .count();
    auto ellapsedTime = (currentTime - startTime)*1e-6;
    std::string value;

    // Continuously read values until flag is true
    while (!stopProfilerThread.load())
    {
        currentTime = std::chrono::duration_cast<std::chrono::nanoseconds>(
                            std::chrono::high_resolution_clock::now().time_since_epoch())
                            .count();
        output << currentTime << ",";

        currFile.seekg(0);
        currFile >> value;
        output << value << ",";
        voltFile.seekg(0);
        voltFile >> value;
        output << value << "\n";
        

        // Compute elapsed time
        ellapsedTime = PROFILER_SLEEP_MS - (currentTime - startTime)*1e-6;
        
        // Adjust the sleep duration based on the desired frequency. 5 milliseconds (200 Hz).
        std::this_thread::sleep_for(std::chrono::milliseconds((long) ellapsedTime));
        startTime = currentTime;
    }

    // Close files
    if (currFile.is_open())
    {
        currFile.close();
    }
    if (voltFile.is_open())
    {
        voltFile.close();
    }
}
