#pragma once

#include "./utils/Kalman2D.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cmath>
#include <vector>
#include <limits>

float minDist = std::numeric_limits<float>::max();
float maxDist, maxTime, minTime = 0;

Kalman2D kf;