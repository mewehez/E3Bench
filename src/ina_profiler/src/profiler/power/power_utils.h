#ifndef __UTILS_H
#define __UTILS_H

#include <fstream>
#include <sstream>

void openFileStream(std::string path, std::ifstream &fileStream, std::ostringstream &errorStream);
#endif
