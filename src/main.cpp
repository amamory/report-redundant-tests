#include <iostream>
#include "greatest.cpp"

using namespace std;

int main(int argc, char** argv)
{
    if(argc != 4) {
        printf("ERROR: expecting 3 ints as arguments!\n");
        return 1;
    }
    const int a = stoi(argv[1]);
    const int b = stoi(argv[2]);
    const int c = stoi(argv[3]);

    cout << "The greatest of " << a << ", " << b << ", " << c << " is " << Greatest(a,b,c) << "\n";
    return 0;
}