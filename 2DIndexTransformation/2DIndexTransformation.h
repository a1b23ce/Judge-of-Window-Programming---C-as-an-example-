#ifndef INDEXTRANSFORMATION_H_
#define INDEXTRANSFORMATION_H_

#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <algorithm>
using namespace std;

#define inputfile_path "FormattedOutput.txt"		// 請替換成您的檔案路徑	(read)
#define outputfile_path "TDTrans.txt"		// 請替換成您的檔案路徑	(write)

struct element
{
	element(int a, float b, float c, float d, float e, string f)
	{
		sequence = a;
		x1 = b;
		y1 = c;
		x2 = d;
		y2 = e;
		word = f;
		middle_x = (b + d) / 2;
		middle_y = (c + e) / 2;
	}
	int sequence;
	float x1;
	float y1;
	float x2;
	float y2;
	string word;
	float middle_x;
	float middle_y;
};

struct element_2D
{
	element_2D()
	{
		sequence = 0;
		x = 0;
		y = 0;
		word = "";
	}
	element_2D(int a, int b, int c, string d)
	{
		sequence = a;
		x = b;
		y = c;
		word = d;
	}
	int sequence;
	int x;
	int y;
	string word;
};

bool isInteger(const std::string& s);
bool isFloat(const std::string& s);
void IndexTrans();

#endif // !INDEXTRANSFORMATION_H_