#include <iostream>
using namespace std;

/*
	#
	##
	###
	####
*/
void stair(int n) 
{
for (int i = 0; i < n; i++)
    {
        for (int j = i; j >= 0; j--) cout << "#";
		cout << endl;
    }   
}

/*
	   #
	  ##
	 ###
	####
*/

void staircase(int n)
{
	for (int i = 0; i < n; i++)
	{
		for (int j = i; j < (n-1); j++)
			cout << " ";
		for (int k = 0; k < (i+1); k++)
			cout << "#";
		cout << "\n";
	}
}

int main()
{
	staircase(4);
	return 0;
}