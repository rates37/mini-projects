#include <math.h>
//  gcc -fPIC -shared -lm -o util.so util.c
void update_grid(int width, int height, double *grid, double *nextGrid, int r_a);
double sigma_1(double x, double a, double alpha);
double sigma_2(double x, double a, double b);
double sigma_m(double x, double y, double m);
double s(double n, double m);
double alpha_m = 0.147;
double alpha_n = 0.028;
double b_1 = 0.278;
double b_2 = 0.365;
double d_1 = 0.267;
double d_2 = 0.445;

double sigma_1(double x, double a, double alpha){
    return 1 / (1 + exp(-(x-a)*4/alpha));
}


double sigma_2(double x, double a, double b){
    return sigma_1(x,a, alpha_n) * (1 - sigma_1(x, b, alpha_n));
}


double sigma_m(double x, double y, double m){
    return x * (1 - sigma_1(m, 0.5, alpha_m)) + y * sigma_1(m, 0.5, alpha_m);
}


double s(double n, double m){
    return sigma_2(n, sigma_m(b_1, d_1, m), sigma_m(b_2, d_2, m));
}

void update_grid(int width, int height, double *grid, double *nextGrid, int r_a) {
    for (int xi = 0; xi < width; xi++) {
        for (int yi = 0; yi < height; yi++) {
            double m = 0;
            double M = 0;
            double n = 0;
            double N = 0;
            double r_i = r_a / 3;

            for (int dx = -(r_a-1); dx < r_a; dx++) {
                for (int dy = -(r_a-1); dy < r_a; dy++) {
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
            nextGrid[yi*width + xi] = 2*s(m/M, n/N) - 1;
        }
    }

    for (int xi = 0; xi < width; xi++) {
        for (int yi = 0; yi < height; yi++) {
            grid[yi*width + xi] += 0.05*nextGrid[yi*width + xi];
            if (grid[yi*width + xi] < 0) grid[yi*width + xi] = 0;
            if (grid[yi*width + xi] > 1) grid[yi*width + xi] = 1;
        }
    }
}
