#include <atomic>
#include <thread>
#include <iostream>
#include <csignal>
#include "vdd_in.h"



// Atomic flag to stop infinite loop of profiler
std::atomic<bool> stopProfilerThread(false);


void ctrlSignalHandler(int signum)
{
    std::cout << "\n[INFO] Ctrl+C pressed. Exiting Profiler program.\n";
    stopProfilerThread.store(true);
    // exit(signum);
}



int main(int argc, char *argv[])
{
    // Ensure that the correct number of arguments are passed
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << "<inteerval_ms> <output_file_path>" << std::endl;
        return 1;
    }

    // Get path to output profiled values
    // fs::path output_dir_path = fs::path(argv[1]);

    std::cout << "[INFO] Running profiler\n";
    // Add signal handler
    std::signal(SIGINT, ctrlSignalHandler);

    // Open output file
    // std::string output_file_path = (output_path / "profiler.csv").string();
    std::ofstream output_file(argv[2]);

    if (!output_file)
    {
        std::cout << "Failed to open output file:\n    " << argv[2] << "\n";
        exit(EXIT_FAILURE);
    }

    // Profile power for rail 1
    int interval = std::atoi(argv[1]);
    readRail1Power(interval, output_file);

    // Wait some milliseconds before stopping
    std::this_thread::sleep_for(std::chrono::milliseconds(10));

    std::cout << "[INFO] -INA- Exiting profiler.\n";
    return 0;
}
