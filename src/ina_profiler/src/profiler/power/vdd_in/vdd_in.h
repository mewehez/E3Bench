#ifndef __VDD_IN_H
#define __VDD_IN_H

#include <fstream>

#define RAIL_ID 1

void readRail1Power(int interval, std::ofstream &output);

#endif