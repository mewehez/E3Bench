#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

#include "board_jon.h"

std::vector<int> getAvailableFrequencies() {
    std::vector<int> frequencies;

    std::ifstream file(GPU_ALL_FREQS);
    if (file.is_open()) {
        std::string line;
        std::getline(file, line);  // Read the entire line from the file

        // Use a stringstream to split the space-separated string
        std::stringstream ss(line);
        std::string frequencyStr;

        // Extract each frequency and convert to an integer
        while (ss >> frequencyStr) {
            try {
                int frequency = std::stoi(frequencyStr);  // Convert the string to an integer
                frequencies.push_back(frequency);
            } catch (const std::invalid_argument& e) {
                std::cerr << "Error: Invalid frequency value: " << frequencyStr << std::endl;
            }
        }
        file.close();
    } else {
        std::cerr << "Error: Could not open file " << GPU_ALL_FREQS << std::endl;
    }

    return frequencies;
}

int main() {
    // Read the frequencies from the file
    std::vector<int> frequencies = getAvailableFrequencies();

    // Print the frequencies in KHz
    if (!frequencies.empty()) {
        std::cout << "Available GPU Frequencies (in KHz):\n";

        for (size_t i = 0; i < frequencies.size(); ++i) {
            if (i > 0) std::cout << ", ";
            std::cout << frequencies[i] / 1000;
        }
        std::cout << "\n";
    } else {
        std::cout << "No frequencies found." << std::endl;
    }

    return 0;
}
