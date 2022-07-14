#include <bits/stdc++.h>
using namespace std;
/*
 * Complete the 'timeConversion' function below.
 *
 * The function is expected to return a STRING.
 * The function accepts STRING s as parameter.
 */
string timeConversion(string s) 
{
    int hrs = stoi(s.substr(0, 2)) % 12;
    if (s[s.length() - 2] == 'P') hrs += 12;
    stringstream ss(to_string(hrs));
    ss << setw(2) << setfill('0') << hrs;
    s.replace(0, 2, ss.str());
    s.pop_back();
    s.pop_back();
    return s;
}
// Autogen by HackerRank
int main()
{
    ofstream fout(getenv("OUTPUT_PATH"));

    string s;
    getline(cin, s);

    string result = timeConversion(s);

    fout << result << "\n";

    fout.close();

    return 0;
}
