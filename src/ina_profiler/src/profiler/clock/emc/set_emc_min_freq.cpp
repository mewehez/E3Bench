#include <fstream>
#include <iostream>
#include <string>
#include <set>
#include <sstream>

#include "board_jon.h"
#include "emc_utils.h"
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
        std::cerr << "Error: Invalid EMC frequency.\n" << getValidFrequenciesMessage(validFrequencies) << "\n";
        return 1;
    }

    // Open frequency value file
    std::ofstream minFreqFile(EMC_MIN_FREQ);

    if (minFreqFile.is_open()) {
        // Write the frequency value received from args to the rate file
        minFreqFile << frequencyValue << "000" << std::endl;

        // Close the file
        minFreqFile.close();

        std::cout << "EMC max frequency set successfully!" << std::endl;
    } else {
        std::cerr << "Error opening the file " <<  EMC_MIN_FREQ << std::endl;
    }

    return 0;
}
