#include <iostream>
#include <fstream>
#include <string>

#include "board_jon.h"

int main() {
    std::ifstream curFreqFile(EMC_CUR_FREQ);
    std::ifstream minFreqFile(EMC_MIN_FREQ);
    std::ifstream maxFreqFile(EMC_MAX_FREQ);

    if (curFreqFile.is_open() && minFreqFile.is_open() && maxFreqFile.is_open()) {
        int curVal, minVal, maxVal;
        minFreqFile >> minVal;
        maxFreqFile >> maxVal;
        curFreqFile >> curVal;

        std::cout << "EMC frequency (Hz)\nMinimum, Maximum, Current\n";
        std::cout << minVal << ", " << maxVal << ", " << curVal << "\n";
    } else {
        std::cerr << "Error opening one or more files.\n";
        return 1;
    }

    return 0;
}
