#include "Analyzer.h"

struct DataPoint{
    int time_ms;
    float distanceCm;
};

int main()
{
    std::ifstream file ("../Arduino/Sensor Test/data/distances_20251027_193920.csv");
    if(!file.is_open()){
        std::cerr << "Error: Couldn't open csv";
        return 1;
    }

    std::vector<DataPoint> data;
    std::string line;

    std::getline(file,line);

    while (std::getline(file,line))
    {
        std::stringstream ss(line);
        std::string timeStr, distStr;

        if(!std::getline(ss,timeStr, ',')) continue;
        if(!std::getline(ss,distStr,',')) continue;

        DataPoint dp;
        dp.time_ms = std::stoi(timeStr);
        dp.distanceCm = std::stof(distStr);

        data.push_back(dp);
    }

    file.close();

    float minDist = std::numeric_limits<float>::max();
    float maxDist = 0;
    
    for (const DataPoint& line : data)
    {
        if (line.distanceCm < minDist) minDist = line.distanceCm;
        if (line.distanceCm > maxDist) maxDist = line.distanceCm;
    }

    std::cout << "Lines: " << data.size() << std::endl;
    std::cout << "Closes Distance: " << minDist << std::endl;
    std::cout << "Furthest Distance: " << maxDist << std::endl;

    return 0;
}