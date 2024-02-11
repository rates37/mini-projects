#include <math.h>
//  gcc -fPIC -shared -lm -o util.so util.c
float update_grid(int width, int height, float *grid, float *nextGrid, int r_a);
float sigma_1(float x, float a, float alpha);
float sigma_2(float x, float a, float b);
float sigma_m(float x, float y, float m);
float s(float n, float m);
float alpha_m = 0.147;
float alpha_n = 0.028;
float b_1 = 0.278;
float b_2 = 0.365;
float d_1 = 0.267;
float d_2 = 0.445;

float sigma_1(float x, float a, float alpha){
    return 1 / (1 + exp(-(x-a)*4/alpha));
}


float sigma_2(float x, float a, float b){
    return sigma_1(x,a, alpha_n) * (1 - sigma_1(x, b, alpha_n));
}


float sigma_m(float x, float y, float m){
    return x * (1 - sigma_1(m, 0.5, alpha_m)) + y * sigma_1(m, 0.5, alpha_m);
}


float s(float n, float m){
    return sigma_2(n, sigma_m(b_1, d_1, m), sigma_m(b_2, d_2, m));
}

float update_grid(int width, int height, float *grid, float *nextGrid, int r_a) {
    for (int xi = 0; xi < width; xi++) {
        for (int yi = 0; yi < height; yi++) {
            float m = 0;
            float M = 0;
            float n = 0;
            float N = 0;
            float r_i = r_a / 3;

            for (int dx = -(r_a-1); dx < r_a; dx++) {
                for (int dy = -(r_a-1); dy < r_a; dx++) {
                    int x = (((xi+dx)%width + width)%width);
                    int y = (((yi+dy)%height + height)%height);
                    if (dx*dx + dy*dy <= r_i * r_i) {
                        m += grid[y*width + x];
                        M++;
                    } else if (dx*dx + dy*dy <= r_a * r_a) {
                        n += grid[y*width + x];
                        N++;
                    }
                }
            }
            nextGrid[yi * width + xi] = 2*s(m/M, n/N) - 1;
        }
    }

    for (int xi = 0; xi < width; xi++) {
        for (int yi = 0; yi < height; yi++) {
            grid[yi * width + xi] += nextGrid[yi * width + xi];
            if (grid[yi * width + xi] > 1) grid[yi * width + xi] = 1;
            if (grid[yi * width + xi] < 0) grid[yi * width + xi] = 0;
        }
    }
}
