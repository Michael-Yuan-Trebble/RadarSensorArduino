#include "Kalman2D.h"

void Kalman2D::Predict(float dt)
{
    px += vx * dt;
    py += vy * dt;

    P[0][0] += dt*(P[2][0]+P[0][2]) + dt*dt*P[2][2] + Q;
    P[1][1] += dt*(P[3][1]+P[1][3]) + dt*dt*P[3][3] + Q;
    P[0][1] += dt*(P[2][1]+P[0][3]) + dt*dt*P[2][3];
    P[1][0] = P[0][1];
}

void Kalman2D::Update(float zx, float zy)
{
    float yx = zx - px;
    float yy = zy - py;

    float Sx = P[0][0] + R;
    float Sy = P[1][1] + R;

    float K00 = P[0][0]/Sx, K10=P[1][0]/Sx, K20=P[2][0]/Sx, K30=P[3][0]/Sx;
    float K01 = P[0][1]/Sy, K11=P[1][1]/Sy, K21=P[2][1]/Sy, K31=P[3][1]/Sy;

    px += K00*yx + K01*yy;
    py += K10*yx + K11*yy;
    vx += K20*yx + K21*yy;
    vy += K30*yx + K31*yy;

    P[0][0] -= K00*P[0][0] + K01*P[0][1];
    P[1][1] -= K10*P[0][1] + K11*P[1][1];
    P[0][1] -= K00*P[0][1] + K01*P[1][1];
    P[1][0] = P[0][1];
}