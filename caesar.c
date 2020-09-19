#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

bool check_key(string s);

int main(int argc, string argv[])
{
    //check valid key provided
    if (argc != 2 || !check_key(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    //convert string to int
    int key = atoi(argv[1]);

    //get plaintext from user
    string plaintext = get_string("plaintext: ");

    //ciphertext
    printf("ciphertext: ");
    for (int i = 0, len = strlen(plaintext); i < len; i++)
    {
        char c = plaintext[i];
        if (isalpha(c))
        {
            char e = 'A';
            if (islower(c))
                e = 'a';
            //changing ascii to alphabetical, calculate and change back
            printf("%c", (c - e + key) % 26 + e);
        }
        else
            printf("%c", c);
    }
    //print new line
    printf("\n");
}

bool check_key(string s)
{
    for (int i = 0, len = strlen(s); i < len; i++)
        if (!isdigit(s[i]))
            return false;
    return true;
}