# pylint: disable=missing-function-docstring, missing-module-docstring/

from numpy import zeros

n = 800
m = 1600
p = 800

a = zeros((n,m))
b = zeros((m,p))
c = zeros((n,p))

#$ omp parallel
#$ omp do schedule(runtime)
for i in range(0, n):
    for j in range(0, m):
        a[i,j] = i-j
#$ omp end do nowait

#$ omp do schedule(runtime)
for i in range(0, m):
    for j in range(0, p):
        b[i,j] = i+j
#$ omp end do nowait

#$ omp do schedule(runtime)
for i in range(0, n):
    for j in range(0, p):
        for k in range(0, p):
            c[i,j] = c[i,j] + a[i,k]*b[k,j]
#$ omp end do
#$ omp end parallel
