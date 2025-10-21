#include <fstream>
#include <sstream>
#include <string>
#include "power_utils.h"

void openFileStream(std::string path, std::ifstream &fileStream, std::ostringstream &errorStream)
{
    fileStream.open(path);
    if (!fileStream.is_open())
    {
        errorStream << "    - " << path << "\n";
    }
}
