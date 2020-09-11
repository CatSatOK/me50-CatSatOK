#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollars;
    //define variable then get user input
   do
   {
        dollars = get_float("How much change is due?\n");
   }
   while (dollars <= 0);
    
    //round up
   int cents = round(dollars * 100);
   int coins = 0;
    
    //find number of coins needed
   while (cents >= 25)
   {
       cents = cents - 25;
       coins++;
   }
   while (cents >= 10)
   {
       cents = cents - 10;
       coins++;
   }
   while (cents >= 5)
   {
       cents = cents - 5;
       coins++;
   }
   while (cents >= 1)
   {
       cents = cents - 1;
       coins++;
   }

    //print result
   printf("Coins needed: %i\n", coins);

}