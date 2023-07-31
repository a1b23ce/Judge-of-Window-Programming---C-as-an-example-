#pragma once

#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <algorithm>
using namespace std;

#define inputfile_path  "D:\\pic\\1-2model.txt"			// 請替換成您的檔案路徑	(read)
#define inputfile_path2 "D:\\pic\\1-2candidate.txt"		// 請替換成您的檔案路徑	(read)
#define outputfile_path "D:\\pic\\1-2new_candidate.txt"	// 請替換成您的檔案路徑	(write)

struct element
{
	element(int a, float b, float c, float d, float e, string f)
	{
		index = a;
		x1 = b;
		y1 = c;
		x2 = d;
		y2 = e;
		word = f;
		middle_x = (b + d) / 2;
		middle_y = (c + e) / 2;
	}
	int index;
	float x1;
	float y1;
	float x2;
	float y2;
	string word;
	float middle_x;
	float middle_y;
};

bool isInteger(const std::string& s);
bool isFloat(const std::string& s);
void FixSeq();