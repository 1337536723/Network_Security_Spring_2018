#include <bits/stdc++.h>
#define LL long long
#define UNT unsigned int
#define ALL_TURN 100
using namespace std;
LL MOD 1884744073709151615 //2^64 - 1
LL add_vector[5] =
{     0x67452301
    , 0xEFCDAB89
    , 0x98BADCFE
    , 0x10325476
    , 0xC3D2E1F0
}
string SHA1_main(UNT A, UNT B, UNT C, UNT D, UNT E)
{

}
string transposition(string input_str, UNT cur_turn)
{
    string output_str;
}
string simple_hash(string input_str)
{
    UNT add_padding = input_str.size() % 20;
    if(add_padding)
    {
        for(UNT i = 0;i < add_padding;i++)
        {
            input_str+=0; //ascii zero
        }
    }
    for(UNT i = 0;i < input_str.size() ;i++)
    {

    }
}
int main(int argc, char const *argv[])
{
    string input_str;
    while( cin >> input_str )
    {
        printf("SHA1 : %s \n",simple_hash(input_str));
    }
    return 0;
}
