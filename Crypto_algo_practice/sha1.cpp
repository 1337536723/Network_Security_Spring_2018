#include <bits/stdc++.h>
#define UNT unsigned int
#define Aunsigned_TURN 100
using namespace std;
unsigned add_vector[4] =
{     0x5A827999
    , 0x6ED9EBA1
    , 0x8F1BBCDC
    , 0xCA62C1D6
};
/*
Pre-processing:
append the bit '1' to the message
append k bits '0', where k is the minimum number >= 0 such that the resulting message
length (in bits) is congruent to 448(mod 512)
append length of message (before pre-processing), in bits, as 64-bit big-endian integer
*/
string preprocessing(string input_str)//add 0 in the end of data
{
    //char is byte by byte, padding 1 in the end
    unsigned original_length = input_str.size() << 3; //append the length of message later in preprocessing, that is why SHA1 Only accept of
    //message of max 2^64 bits
    input_str += (char) 0x80; //0b10000000
    while(input_str.size() << 3 % 512 != 448) //1 char is 8 bits, we process bitwise rather than bytewise
    {
        input_str += (char) 0;
    }
    cout<<"After padding to 448 mod 512 input_str become: "<<input_str<<" with its length in bits "<<(input_str.size()<<8)<<endl;
    //append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    unsigned append_value = original_length & 0xFFFFFFFFFFFFFFFF;
    while( append_value )
    {
        input_str += (char) ( append_value & 0xFF );
        append_value >>= 8; //bitwise processing
    }
    cout<<"After padding to 0 mod 512 input_str become: "<<input_str<<" with its length in bits "<<(input_str.size()<<8)<<endl;
    return input_str;
}
unsigned left_rotate(unsigned orginal_value, int bits, int all_length)
{
    return (orginal_value << bits | orginal_value >> (all_length - bits));
}
vector<unsigned> one_block_processing(string input_str_blocksubstr)  //one_block_processing of 512 bits long
{
    unsigned int buffer_str[16]={0};
    for(int i = 0 ; i < 16 ; i++)//each word is 32 bits and there are 16 words in a given block to per processed
    {
        // buffer_str[i] = ((unsigned int)input_str_blocksubstr.substr( i * 4, 4) & 0xFFFFFFFF ); casting problem
        buffer_str[i]=((unsigned)input_str_blocksubstr[i * 4] & 0xFF)<<24 |
                 ((unsigned)input_str_blocksubstr[i * 4 + 1] & 0xFF)<<16 |
                 ((unsigned)input_str_blocksubstr[i * 4 + 2] & 0xFF)<<8 |
                 ((unsigned)input_str_blocksubstr[i * 4 + 3] & 0xFF); //bit wise concatenation
    }
    vector<unsigned> final_buffer(80,0);
    for(int i = 16 ; i < 80 ; i++)
    {
        final_buffer[i] = buffer_str[i - 3] ^ buffer_str[i - 8] ^ buffer_str[i - 14] ^ buffer_str[i - 16];
        final_buffer[i] = left_rotate((unsigned)final_buffer[i], i, 32); //circular shifiting code !!
    }
    return final_buffer;
}

UNT nonlinear_transform(UNT A, UNT B, UNT C, UNT D, UNT E, UNT cur_round) //non linear transform
{
    if( cur_round >= 0 && cur_round < 20)
    {
        return (B & C) | ((~B) & D);
    }
    else if( cur_round >= 20 && cur_round < 40)
    {
        return B ^ C ^ D;
    }
    else if( cur_round >= 40 && cur_round < 60)
    {
        return (B & C) | (B & D) | (C & D);
    }
    else if( cur_round >= 60 && cur_round < 80)
    {
        return B ^ C ^ D;
    }
    return (B & C) | (B & D) | (C & D); //for compile OK
}


string sha1_main(string input_str)
{
    input_str = preprocessing(input_str);
    cout<<"Size after preprocessing"<<(input_str.size()<<8)<<endl;
    unsigned A = 0x67452301;
    unsigned B = 0xEFCDAB89;
    unsigned C = 0x98BADCFE;
    unsigned D = 0x10325476;
    unsigned E = 0xC3D2E1F0;
    unsigned F = 0, K = 0, temp = 0;
    unsigned H0 = 0, H1 = 0, H2 = 0, H3 = 0, H4 = 0;
    vector<unsigned> one_block_str;

    for(int processed_byte = 0 ; processed_byte != input_str.size() ; processed_byte += 64)
    //process 512 per block operation, 512 = 64bytes = 64chars
    {
        one_block_str = one_block_processing(input_str.substr(processed_byte , 64)); //feed a length of 64 bytes (or say 512 bits) long string
        for(int i = 0 ; i < 80 ; i++)
        {
            K = add_vector[i / 20];
            F = nonlinear_transform(A, B, C, D, E, i);
            temp = left_rotate(A, 5 ,32) + F + E + K + ( ((unsigned)one_block_str[i]) & 0xFFFFFFFF);
            E = D;
            D = C;
            C = left_rotate(B, 30 ,32);
            B = A;
            A = temp;
        }
        one_block_str.clear();
        H0 += A;
        H1 += B;
        H2 += C;
        H3 += D;
        H4 += E;
    }
    cout<<"SHA 1: "<<std::hex<<H0<<H1<<H2<<H3<<H4<<endl;
}
int main(int argc, char const *argv[])
{
    string input_str;
    while( cin >> input_str )
    {
        sha1_main(input_str);
    }
    return 0;
}
