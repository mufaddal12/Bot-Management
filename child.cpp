#include <iostream>

using namespace std;

int main()
{
    char line[20];
    cin >> line;
    line[9] = '-';
    line[10] = 'C';
    line[11] = line[12] = 'P';
    line[13] = 0;
    cout << line;
    return 0;
}