// Digital root
#include <iostream>
using namespace std;
int digital_root(int n)
{
	int sum = 0;
	while (n != 0) {sum += (n % 10); n = n / 10;};
	cout << sum << endl;
if (sum / 10 > 0) {digital_root(sum); return n;}
	else return sum;
}
int main()
{
	digital_root(132189);
	return 0;
}