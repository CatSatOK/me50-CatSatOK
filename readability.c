#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <ctype.h>
#include <string.h>

int main(void)
{
    //prompt for text and assign variables

    string text = get_string("Text: \n");
    int letters = 0;
    int words = 1;
    int sentances = 0;

    //count letters
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    //count words
    for (int i = 1, len = strlen(text); i < len; i++)
    {
        if ((isgraph(text[i])) && (isspace(text[i + 1])))
        {
            words++;
        }
    }
    //count sentances
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentances++;
        }
    }

    //find L & S
    //need to cast ints as floats first to return a float
    float L = ((float)letters / (float)words) * 100;
    float S = ((float)sentances / (float)words) * 100;

    // run Coleman-Liau and round result
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    //print grade results
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}