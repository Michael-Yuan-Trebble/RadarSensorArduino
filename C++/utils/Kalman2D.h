#pragma once

class Kalman2D{ 
    public:
        float px=0, py=0,vx=0,vy=0;
        float x[4] = {0,0,0,0};

        float P[4][4] = {1,0,0,0,
                        0,1,0,0,
                        0,0,1,0,
                        0,0,0,1};

        float Q = 0.01f;
        float R = 0.1f;

        void Predict(float dt);

        void Update(float zx, float zy);
};