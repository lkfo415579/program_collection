//matrix_add.cu
//这个文件不推荐直接拷贝，最好一行一行地抄下来
#include <stdio.h>

#define N 1024  //这里定义了矩阵的阶级，这里用一个32x32的方形矩阵做例子
//想要自己Debug的时候，遇到问题，可以先把N的值设置小一些，比如4
#define THREAD_NUM 32
#define BLOCK_NUM 32
/*
 * 本次的核函数，三个参数分别是两个NxN的输入矩阵和一个NxN的输出矩阵
 */
__global__ void matrix_add(const int a[][N], const int b[][N], int c[][N]) {
    int idx = threadIdx.x;
    int idy = threadIdx.y;
    int bidx = blockIdx.x;
    int bidy = blockIdx.y;
    int realx = THREAD_NUM * bidx + idx;
    int realy = THREAD_NUM * bidy + idy;
    //printf("idx[%d],idy[%d]\n", idx, idy );
    //printf("realx[%d],realy[%d],bidx[%d]\n", realx,realy,bidx );
    //printf("bidx[%d]\n", bidx );
    //int idy = threadIdx.y;
    //printf ("a[idx][idy]:%d,idx[%d],idy[%d]\n", a[idx][idy], idx, idy );
    //printf ("a:%d,realx[%d],realy[%d]\n", a[realx][realy], realx, realy );
    c[realx][realy] = a[realx][realy] + b[realx][realy];
}

int main(void) {

    int *h_a, *h_b, *h_c;
    int *dev_a, *dev_b, *dev_c;

    //这里把一个block的里面的线程排列定义成二维的，这样会有两个维度的索引值，x和y
    dim3 threads_in_block (THREAD_NUM, THREAD_NUM);
    //err这个值是用来检查cuda的函数是否正常运行的
    cudaError_t err = cudaSuccess;

    h_a = (int *)malloc(sizeof(int) * N * N);
    h_b = (int *)malloc(sizeof(int) * N * N);
    h_c = (int *)malloc(sizeof(int) * N * N);

    if (h_a == NULL || h_b == NULL || h_c == NULL) {
        fprintf(stderr, "Malloc() failed.\n");
        return -1;
    }

    err = cudaMalloc((void **)&dev_a, sizeof(int) * N * N);
    if (err != cudaSuccess) {
        fprintf(stderr, "cudaMalloc() failed.\n");
        return -1;
    }
    err = cudaMalloc((void **)&dev_b, sizeof(int) * N * N);
    if (err != cudaSuccess) {
        fprintf(stderr, "cudaMalloc() failed.\n");
        return -1;
    }
    err = cudaMalloc((void **)&dev_c, sizeof(int) * N * N);
    if (err != cudaSuccess) {
        fprintf(stderr, "cudaMalloc() failed.\n");
        return -1;
    }

    for (int i = 0; i < N * N; i++) {
        h_a[i] = 2 * i + 1;
        h_b[i] = -1 * i + 5;
        //printf("a[%d]%d ", i, h_a[i] );
        //if (i % N == 0 && i != 0)
        //  printf("\n");
    }
    printf("\n--------------\n");
    //for (int i = 0; i < N * N; i++) {
      //printf("b[%d]%d ", i, h_b[i] );
      //if (i % N == 0 && i != 0)
        //printf("\n");
    //}
    //printf("\n");

    err = cudaMemcpy(dev_a, h_a, sizeof(int) * N * N, cudaMemcpyHostToDevice);
    if (err != cudaSuccess) {
        fprintf(stderr, "cudaMemcpy() failed.\n");
        return -1;
    }
    err = cudaMemcpy(dev_b, h_b, sizeof(int) * N * N, cudaMemcpyHostToDevice);
    if (err != cudaSuccess) {
        fprintf(stderr, "cudaMemcpy() failed.\n");
        return -1;
    }

    matrix_add<<<threads_in_block, threads_in_block>>>((int (*)[N])dev_a, (int (*)[N])dev_b, (int (*)[N])dev_c);

    err = cudaMemcpy(h_c, dev_c, sizeof(int) * N * N, cudaMemcpyDeviceToHost);
    if (err != cudaSuccess) {
        fprintf(stderr, "cudaMemcpy() failed.\n");
        return -1;
    }
    printf("done2.\n");
    for (int i = 0; i < N * N; i++) {
        if (h_a[i] + h_b[i] != h_c[i]) {
            fprintf(stderr, "a[%d]%d + b[%d]%d != c[%d]%d.\n", i, h_a[i], i, h_b[i], i, h_c[i]);
            return -1;
        }
    }
    for (int i = 0; i < N*N; i++) {
        printf("c[%d]%d ", i, h_c[i] );
        if (i % N == 0 && i != 0)
          printf("\n");
        if (i > 20)
          break;
    }
    printf("\nsize of c[]:%d\n",  N * N );
    //printf("\n");
    printf("done.\n");
    return 0;
}
