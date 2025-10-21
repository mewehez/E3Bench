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

    // Open the files and write values to them
    std::ofstream mrqRateLockedFile(MRQ_RATE_LOCK);
    std::ofstream stateFile(EMC_STATE);
    std::ofstream rateFile(EMC_CUR_FREQ);

    if (mrqRateLockedFile.is_open() && stateFile.is_open() && rateFile.is_open()) {
        // Write fixed values to mrq_rate_locked and state
        mrqRateLockedFile << "1" << std::endl;
        stateFile << "1" << std::endl;

        // Write the frequency value received from args to the rate file
        rateFile << frequencyValue << "000" << std::endl;

        // Close the files
        mrqRateLockedFile.close();
        stateFile.close();
        rateFile.close();

        std::cout << "EMC current frequency set successfully!" << std::endl;
    } else {
        std::cerr << "Error opening one or more files." << std::endl;
    }

    return 0;
}
