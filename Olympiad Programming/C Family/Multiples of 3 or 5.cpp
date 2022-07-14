// Multiples of 3 or 5
#include <iostream>
using namespace std;
int solution(int number)
{
	int sum = 0;
	for (int i = 0; i < number; i++)
	{
		if ((i % 3 == 0) || (i % 5 == 0)) sum += i;
	};
	// cout << sum;
	return sum;
};
int main()
{
	solution(10);
	return 0;
};