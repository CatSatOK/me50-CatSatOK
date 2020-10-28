#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i=0; i<height; i++)
    {
        for (int j=0; j<width; j++)
        {
            float average = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue)/3.00;
            int avg = round(average);

            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i=0; i<height; i++)
    {
        for (int j=0; j<width; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            image[i][j].rgbtRed = (sepiaRed > 255) ? 255 : sepiaRed;
            image[i][j].rgbtGreen = (sepiaGreen > 255) ? 255 : sepiaGreen;
            image[i][j].rgbtBlue = (sepiaBlue > 255) ? 255 : sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i=0; i<height; i++)
    {
        for (int j=0; j<width/2; j++)
        {
           int red = image[i][j].rgbtRed;
           int green = image[i][j].rgbtGreen;
           int blue = image[i][j].rgbtBlue;

           image[i][j].rgbtRed = image[i][width - j - 1].rgbtRed;
           image[i][j].rgbtGreen = image[i][width - j - 1].rgbtGreen;
           image[i][j].rgbtBlue = image[i][width - j - 1].rgbtBlue;

           image[i][width - j - 1].rgbtRed = red;
           image[i][width - j - 1].rgbtGreen = green;
           image[i][width - j - 1].rgbtBlue = blue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // make temp copy of image
    RGBTRIPLE temp[height][width];

    for (int i=0; i<height; i++)
    {
        for (int j=0; j<width; j++)
        {
            int sumRed = 0;
            int sumGreen = 0;
            int sumBlue = 0;
            float counter = 0;

            for (int w=-1; w<2; w++)
            {
                for (int h=-1; h<2; h++)
                {
                    if(i + w < 0 || i + w > height -1 || j + h < 0 || j + h > width -1)
                    {
                        continue;
                    }

                    sumRed += image[i+w][j+h].rgbtRed;
                    sumGreen += image[i+w][j+h].rgbtGreen;
                    sumBlue += image[i+w][j+h].rgbtBlue;

                    counter++;
                }
            }

            temp[i][j].rgbtRed = round(sumRed/counter);
            temp[i][j].rgbtGreen = round(sumGreen/counter);
            temp[i][j].rgbtBlue = round(sumBlue/counter);
        }
    }

    for (int i=0; i<height; i++)
    {
        for (int j=0; j<width; j++)
        {
           image[i][j].rgbtRed = temp[i][j].rgbtRed;
           image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
           image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }
    return;
}
