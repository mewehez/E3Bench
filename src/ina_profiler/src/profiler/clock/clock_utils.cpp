#include <set>
#include <string>
#include <sstream>

#include "clock_utils.h"

// Function to check if a given frequency is in the predefined list
bool isValidFrequency(const std::string& freqStr, const std::set<int>& validFrequencies) {
    int freq;
    std::stringstream(freqStr) >> freq;  // Convert string to integer
    return validFrequencies.find(freq) != validFrequencies.end();
}

// Function to construct the valid frequencies message using stringstream
std::string getValidFrequenciesMessage(const std::set<int>& validFrequencies) {
    std::stringstream message;
    message << "Valid frequencies are: ";

    for (auto it = validFrequencies.begin(); it != validFrequencies.end(); ++it) {
        if (it != validFrequencies.begin()) {
            message << ", ";  // Add comma between values
        }
        message << *it;  // Append the frequency to the message
    }

    return message.str();  // Convert the stringstream to a string and return it
}
