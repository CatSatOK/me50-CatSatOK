#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int number, line, hash, dot;
    //request input
    do
    {
        number = get_int("What height do you want the pyramid?\n");
    }
    //ensure keeps to size requirements
    while (number < 1 || number > 8);
    //make pyramid
    for (line = 0; line < number; line++)
    {
        for (dot = 0; dot < number - line - 1; dot++)
        {
            printf(" ");
        }
        for (hash = 0; hash <= line; hash++)
        {
            printf("#");
        }
        printf("\n");
    }
}