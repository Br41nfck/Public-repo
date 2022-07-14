#include <iostream>
#include <vector>
using namespace std;

class Solution
{
	public:
	int findNumbers(vector<int>& nums)
	{
		int res = 0;
		
		for (int i = 0; i < nums.size(); i++)
		{
			int count = 0;
			while (nums[i] != 0)
			{
				nums[i] = nums[i] / 10;
				count++;
			}
			//cout << count << endl;
			//cout << endl;
			if (count % 2 == 0) res++;
		}
		
		
		//cout <<  "res: " << res << endl;
		return res;
	};
};

int main()
{
	Solution o;
	vector<int> t = {555,901,482,1771};
	o.findNumbers(t);
	return 0;
}