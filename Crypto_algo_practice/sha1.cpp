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
UNT mixing_values(UNT A, UNT B, UNT C, UNT D, UNT E, UNT cur_turn)
{
    if( cur_turn >= 0 && cur_turn < 20)
    {

    }
    else if( cur_turn >= 20 && cur_turn < 40)
    {

    }
    else if( cur_turn >= 40 && cur_turn < 60)
    {

    }
    else if( cur_turn >= 60 && cur_turn < 80)
    {

    }
}
string transposition(string input_str, UNT cur_turn)
{
    string output_str;
}
void preprocessing(string input_str)//add 0 in the end of data
{
    //char is byte by byte, padding 1 in the end
    input_str += (unsigned char) 0x80; //0b10000000
    while(input_str.size() << 3 % 512 != 448) //1 char is 8 bits, we process bitwise rather than bytewise
    {
        str += (unsigned char)0;
    }
}
void break_messsge(string input_str) //break message into several 512-bit chunks
{
    
}
string sha1_main(string input_str)
{
    UNT add_padding = input_str.size() % 20;
    if(add_padding)
    {
        for(UNT i = 0;i < add_padding;i++)
        {
            input_str += 0; //ascii zero
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
