#ifndef __CLOCK_UTILS_H
#define __CLOCK_UTILS_H

#include <set>
#include <string>

// const std::set<int> validFrequencies = {204000, 2133000, 665600};
bool isValidFrequency(const std::string& freqStr, const std::set<int>& validFrequencies);
std::string getValidFrequenciesMessage(const std::set<int>& validFrequencies);

#endif
