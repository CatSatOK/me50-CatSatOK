#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#define BLOCKSIZE 512

//make input error return
int inputError()
{
    printf("Usage: ./recover image\n");
    return 1;
}

//make file error return
int fileError(char filename[])
{
    printf ("Unable to open file: %s\n", filename);
    return 1;
}

//make if jpg header
bool isJpgHeader (uint8_t buffer[])
{
    return buffer[0] == 0xff
    && buffer[1] == 0xd8
    && buffer[2] == 0xff
    && (buffer[3] & 0xf0) ==0xe0;
}

//main
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return inputError();
    }

    char * inputFile = argv[1];
    if (inputFile == NULL)
    {
        return inputError();
    }

    //make file pointer & error check
    FILE* inputPtr = fopen(inputFile, "r");
    if (inputPtr == NULL)
    {
        return fileError(inputFile);
    }

    char filename[8];
    FILE* outputPtr = NULL;
    uint8_t buffer[BLOCKSIZE];
    int jpgCounter = 0;

    while (fread (buffer, sizeof(uint8_t), BLOCKSIZE, inputPtr) || feof(inputPtr) == 0)
    {
        if(isJpgHeader(buffer))
        {
            sprintf(filename, " %03i.jpg", jpgCounter);
            outputPtr = fopen(filename, "w");
            jpgCounter++;
        }
        if(outputPtr != NULL)
        {
            fwrite(buffer, sizeof(buffer), 1, outputPtr);
        }
    }
     if(inputPtr != NULL)
    {
        fclose(inputPtr);
    }

    if(outputPtr != NULL)
    {
        fclose(outputPtr);
    }
    return 0;
}
