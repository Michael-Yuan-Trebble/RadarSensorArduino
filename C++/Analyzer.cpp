#include "Analyzer.h"

struct DataPoint{
    int timeMs;
    float dt;
    float distanceCm;
    int angle;
};

int main(int argc, char* argv[])
{
    if (argc < 2) return 1;
    std::string fileName = argv[1];
    std::ifstream file (fileName);

    if(!file.is_open())
    {
        std::cerr << "Error: Couldn't open csv";
        return 1;
    }

    std::vector<DataPoint> data;
    std::string line;

    std::getline(file,line);

    while (std::getline(file,line))
    {
        std::stringstream ss(line);
        std::string timeStr, distStr, dt, angle;

        if(!std::getline(ss,timeStr, ',')) continue;
        if(!std::getline(ss,dt,',')) continue;
        if(!std::getline(ss,distStr,',')) continue;
        if(!std::getline(ss,angle,',')) continue;

        DataPoint dp;
        dp.timeMs = std::stoi(timeStr);
        dp.dt = std::stoi(dt) * 1e-6f;
        dp.distanceCm = std::stof(distStr);
        dp.angle = std::stoi(angle);

        data.push_back(dp);
    }

    file.close();

    long longestY = 0;
    
    for (const DataPoint& line : data)
    {
        kf.Predict(line.dt);
        float mx = line.distanceCm * cos(line.angle);
        float my = line.distanceCm * sin(line.angle);
        kf.Update(mx,my);
        if (line.distanceCm < minDist) 
        {
            minDist = line.distanceCm;
            minTime = line.timeMs;
        }
        else if (line.distanceCm > maxDist) 
        {
            maxDist = line.distanceCm;
            maxTime = line.timeMs;
        }
        if (kf.py > longestY)
        {
            longestY = kf.py;
        }
    }

    std::cout << "Lines: " << data.size() << std::endl;
    std::cout << "Closest Distance: " << minDist << " at Time: " << minTime << std::endl;
    std::cout << "Furthest Distance: " << maxDist << " at Time: " << maxTime << std::endl;
    std::cout << "Debug: " << longestY << std::endl;
    return 0;
}