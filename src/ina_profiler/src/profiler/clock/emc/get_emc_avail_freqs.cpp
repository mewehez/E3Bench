#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <dirent.h>
#include <cstring>
#include <regex>
#include <filesystem>

#include "board_jon.h"

namespace fs = std::filesystem;

// Function to get the list of available frequencies
std::vector<int> getAvailableFrequencies() {
    fs::path dirPath = EMC_ALL_FREQS; 
    std::regex pattern("^[0-9]+$");
    std::vector<int> frequencies;

    // Loop through the files and folders in the directory
    for (const auto& entry : fs::directory_iterator(dirPath)) {
        // Get the name of the file/folder
        std::string filename = entry.path().filename().string();

        // Check if the filename matches the pattern
        int freq;
        if (std::regex_match(filename, pattern)) {
            // std::cout << "Match found: " << filename << std::endl;
            std::stringstream(filename) >> freq;
            frequencies.push_back(freq);
        }
    }

    return frequencies;
}


int main() {
    // Get the list of available frequencies
    std::vector<int> frequencies = getAvailableFrequencies();

    // Print the list of available frequencies
    if (!frequencies.empty()) {
        std::cout << "Available EMC frequencies (in KHz): \n";
        for (size_t i = 0; i < frequencies.size(); ++i) {
            if (i > 0) std::cout << ", ";
            std::cout << frequencies[i];
        }
        std::cout << "\n";
    } else {
        std::cerr << "No valid frequencies found.\n";
    }

    return 0;
}
