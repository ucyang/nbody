#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char *argv[])
{
    long long nsteps;
    long long nparticles;

    double *m;
    double *x, *y, *z;
    double *x_tmp, *y_tmp, *z_tmp;
    double *vx, *vy, *vz;

    double G;
    double dt;
    double dx, dy, dz;
    double r, a;
    double softening;

    long long n, i, j;

    FILE *f;

    if (argc < 6) {
        puts("Please specify arguments correctly.\n\n"
            "Usage: nbody <nsteps> <dt> <G> <softening> <PARAMETERS_FILE>\n\n"
            "PARAMETERS_FILE format:\n"
            " nparticles (on the first line)\n"
            " m x y z vx vy vz (on each line after the first line)");
        return 0x1;
    }

    nsteps = atoll(argv[1]);
    dt = atof(argv[2]);
    G = atof(argv[3]);
    softening = atof(argv[4]);

    f = fopen(argv[5], "r");
    if (!f) {
        printf("Can't open the PARAMETERS_FILE: %s\n", argv[5]);
        return 0x2;
    }

    fscanf(f, "%lld", &nparticles);
    m = (double *)malloc(nparticles * sizeof(double));
    x = (double *)malloc(nparticles * sizeof(double));
    y = (double *)malloc(nparticles * sizeof(double));
    z = (double *)malloc(nparticles * sizeof(double));
    x_tmp = (double *)malloc(nparticles * sizeof(double));
    y_tmp= (double *)malloc(nparticles * sizeof(double));
    z_tmp = (double *)malloc(nparticles * sizeof(double));
    vx = (double *)malloc(nparticles * sizeof(double));
    vy = (double *)malloc(nparticles * sizeof(double));
    vz = (double *)malloc(nparticles * sizeof(double));

    puts("Initial parameters:");
    for (i = 0; i < nparticles; i++) {
        fscanf(f, "%lf %lf %lf %lf %lf %lf %lf",
            &m[i], &x[i], &y[i], &z[i], &vx[i], &vy[i], &vz[i]);
        printf("%lld : m = %lg x = %lg y = %lg z = %lg "
            "vx = %lg vy = %lg vz = %lg\n",
            i, m[i], x[i], y[i], z[i], vx[i], vy[i], vz[i]);
    }
    fclose(f);

    puts("n = 0");
    for (i = 0; i < nparticles; i++)
        printf("%lld : %lg %lg %lg\n", i, x[i], y[i], z[i]);

    #pragma omp parallel private(n, j, dx, dy, dz, r, a)
    for (n = 1; n <= nsteps; n++) {
        #pragma omp for
        for (i = 0; i < nparticles; i++) {
            x_tmp[i] = x[i] + vx[i] * dt;
            y_tmp[i] = y[i] + vy[i] * dt;
            z_tmp[i] = z[i] + vz[i] * dt;

            for (j = 0; j < nparticles; j++) {
                dx = x[j] - x[i];
                dy = y[j] - y[i];
                dz = z[j] - z[i];

                r = sqrt(dx * dx + dy * dy + dz * dz + softening);
                a = G * m[j] / (r * r * r) * dt;

                vx[i] += a * dx;
                vy[i] += a * dy;
                vz[i] += a * dz;
            }
        }

        #pragma omp for
        for (i = 0; i < nparticles; i++) {
            x[i] = x_tmp[i];
            y[i] = y_tmp[i];
            z[i] = z_tmp[i];
        }

        #pragma omp master
        {
        printf("n = %lld\n", n);
        for (i = 0; i < nparticles; i++)
            printf("%lld : %lg %lg %lg\n", i, x[i], y[i], z[i]);
        }
    }

    free(m);
    free(x);
    free(y);
    free(z);
    free(x_tmp);
    free(y_tmp);
    free(z_tmp);
    free(vx);
    free(vy);
    free(vz);

    return 0;
}
