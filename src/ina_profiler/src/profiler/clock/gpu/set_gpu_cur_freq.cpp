#include <fstream>
#include <iostream>
#include <string>
#include <set>
#include <sstream>

#include "board_jon.h"
#include "gpu_utils.h"
#include "clock_utils.h"

int main(int argc, char* argv[]) {
    // Ensure that the correct number of arguments are passed
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <frequency_value>" << std::endl;
        return 1;
    }

    // The frequency value passed as the first argument
    std::string frequencyValue = argv[1];

    // Check if the frequency is valid
    if (!isValidFrequency(frequencyValue, validFrequencies)) {
        std::cerr << "Error: Invalid GPU frequency.\n" << getValidFrequenciesMessage(validFrequencies) << "\n";
        return 1;
    }

    // Open the files and write values to them
    std::ofstream maxFreqFile(GPU_MAX_FREQ);
    std::ofstream minFreqFile(GPU_MIN_FREQ);

    if (maxFreqFile.is_open() && minFreqFile.is_open()) {
        // Write values to min and max frequency files
        maxFreqFile << frequencyValue << "000" << std::endl;
        minFreqFile << frequencyValue << "000" << std::endl;

        // Close the files
        maxFreqFile.close();
        minFreqFile.close();

        std::cout << "GPU current frequency set successfully!" << std::endl;
    } else {
        std::cerr << "Error opening one or more files." << std::endl;
    }

    return 0;
}

