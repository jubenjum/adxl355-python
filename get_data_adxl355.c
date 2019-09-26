
#include <stdio.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>
#include <i2c/smbus.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <string.h>

#define READ_BIT 0x01
#define WRITE_BIT 0x00
#define DUMMY_BYTE 0xAA
#define MEASURE_MODE 0x06 // Only accelerometer

#define DEVICE_ADDRESS 0x1D
#define DEVICE_REG_MODE1 0x00
#define DEVICE_REG_LEDOUT0 0x1d 

// Addresses
#define XDATA3 0x08
#define XDATA2 0x09
#define XDATA1 0x0A
#define YDATA3 0x0B
#define YDATA2 0x0C
#define YDATA1 0x0D
#define ZDATA3 0x0E
#define ZDATA2 0x0F
#define ZDATA1 0x10
#define RANGE 0x2C
#define POWER_CTL 0x2D

#define AXIS_START XDATA3
#define AXIS_LENGTH 9


// Data Range
#define RANGE_2G 0x01

#define I2C_FILE_NAME "/dev/i2c-1"


int main(int argc, char **argv) {
    int i2c_file;
    float axisX, axisY, axisZ;
    char *axisBytes;
    axisBytes = malloc(9); // I will read 3 * 3 bytes 

    // Open a connection to the I2C userspace control file.
    if ((i2c_file = open(I2C_FILE_NAME, O_RDWR)) < 0) {
        perror("Unable to open i2c control file");
        exit(1);
    }

    // configuring the adxl355 ... ioctl ...
    if (ioctl(i2c_file, I2C_SLAVE, 0x1D) < 0) {
            /* ERROR HANDLING; you can check errno to see what went wrong */
        perror("cannot configure ioctl");
         exit(1);
    }

    if (i2c_smbus_write_word_data(i2c_file, RANGE, RANGE_2G)) {
        perror("couldn't configure RANGE");
        exit(1);
    }


    if ( i2c_smbus_write_word_data(i2c_file, POWER_CTL, MEASURE_MODE))  {
        perror("couldn't configure POWER_CTL");
        exit(1);
    }

    FILE *fd;
    fd = fopen("toto.txt", "w");
    while (1) {
        // read the values
        i2c_smbus_read_i2c_block_data(i2c_file, AXIS_START, AXIS_LENGTH, axisBytes);
        axisX = (axisBytes[0] << 16 | axisBytes[1] << 8 | axisBytes[2]) >> 4;
        axisY = (axisBytes[3] << 16 | axisBytes[4] << 8 | axisBytes[5]) >> 4;
        axisZ = (axisBytes[6] << 16 | axisBytes[7] << 8 | axisBytes[8]) >> 4;
        //printf("X = %d\tY = %d\tZ = %d\n", axisX, axisY, axisZ); 
        fprintf(fd, "X = %d\tY = %d\tZ = %d\n", axisX, axisY, axisZ); 
    }

    close(i2c_file);
    fclose(fd);
    free(axisBytes);
    return 0;
}

