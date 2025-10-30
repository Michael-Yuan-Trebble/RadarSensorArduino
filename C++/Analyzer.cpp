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

    std::string from = "data";
    std::string outFileName = fileName;
    std::string to = "analyzed";
    size_t pos = outFileName.find(from);
    if (pos != std::string::npos) 
    {
        outFileName.replace(pos, from.length(), to);
    }
    
    std::ofstream outFile (outFileName);

    if(!file.is_open())
    {
        std::cerr << "Error: Couldn't open csv";
        return 1;
    }

    if(!outFile.is_open())
    {
        std::cerr << "Failed to create file at: " << outFileName;
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
    
    for (const DataPoint& line : data)
    {
        kf.Predict(line.dt);
        float mx = line.distanceCm * cos(line.angle);
        float my = line.distanceCm * sin(line.angle);
        kf.Update(mx,my);

        float distance = std::sqrt(kf.px*kf.px + kf.py*kf.py);

        if (distance < minDist) 
        {
            minDist = distance;
            minTime = line.timeMs;
        }
        else if (distance > maxDist) 
        {
            maxDist = distance;
            maxTime = line.timeMs;
        }
    }

    outFile << "minTime(s),minDistance(cm),maxTime(s),maxDistance(cm)\n";
    outFile << minTime << "," << minDist << "," << maxTime << "," << maxDist;

    outFile.close();

    std::cout << "Lines: " << data.size() << std::endl;
    std::cout << "Closest Distance: " << minDist << " at Time: " << minTime << std::endl;
    std::cout << "Furthest Distance: " << maxDist << " at Time: " << maxTime << std::endl;
    return 0;
}