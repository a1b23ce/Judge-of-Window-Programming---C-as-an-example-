#include "2DIndexTransformation.h"

bool isInteger(const std::string& s)
{
	try
	{
		size_t pos = 0;
		std::stoi(s, &pos);
		return pos == s.length(); // 確保整個字串都轉換為整數
	}
	catch (const std::exception& e)
	{
		return false; // 轉換失敗，不是整數
	}
}

bool isFloat(const std::string& s)
{
	try
	{
		size_t pos = 0;
		std::stof(s, &pos);
		return pos == s.length(); // 確保整個字串都轉換為浮點數
	}
	catch (const std::exception& e)
	{
		return false; // 轉換失敗，不是浮點數
	}
}

void IndexTrans()
{
	vector <element> ELEMENT;
	vector <element_2D> ELEMENT_2D;
	vector <string> elements;
	vector <float> element_x2;	//rightmost ,水平線的LINE, edge survival method
	vector <float> element_y2;	//垂直線的LINE, edge survival method
	string temp_line;

	ifstream file(inputfile_path);			//read file
	if (!file.is_open())
	{
		cout << "無法開啟檔案：" << inputfile_path << endl;
		return;
	}
	ofstream output_file(outputfile_path);	//write file

	while (getline(file, temp_line))
	{
		elements.clear();

		stringstream ss(temp_line);
		string item;
		int item_number = 0;
		while (getline(ss, item, '@'))		//以@符號分隔元件
		{
			elements.push_back(item);
			item_number++;
		}

		if (item_number == 6)				//保險機制
		{
			if (isInteger(elements[0]) && isFloat(elements[1]) && isFloat(elements[2]) && isFloat(elements[3]) && isFloat(elements[4]))
			{
				ELEMENT.push_back(element(atoi(elements[0].c_str()), stof(elements[1]), stof(elements[2]), stof(elements[3]), stof(elements[4]), elements[5]));
			}
		}
	}

	for (int i = 0; i < ELEMENT.size(); i++)
	{
		element_x2.push_back(ELEMENT[i].x2);		//垂直線
		element_y2.push_back(ELEMENT[i].y2);		//水平線
		ELEMENT_2D.push_back(element_2D());			//轉換成2D
	}

	sort(element_x2.begin(), element_x2.end());	//以小到大(左到右)
	sort(element_y2.begin(), element_y2.end());	//以小到大(上到下)
	element_x2.erase(unique(element_x2.begin(), element_x2.end()), element_x2.end());	//刪除重複元素
	element_y2.erase(unique(element_y2.begin(), element_y2.end()), element_y2.end());	//刪除重複元素

	int coordinate_x = 1;
	bool* placed_ELEMENT = new bool[ELEMENT.size() + 5];		//已放置/未放置
	for (int i = 0; i < ELEMENT.size() + 5; i++)
		placed_ELEMENT[i] = false;
	for (int i = 0; i < element_x2.size(); i++)					//垂直線
	{
		bool have_element = false;
		for (int j = 0; j < ELEMENT.size(); j++)
			if (ELEMENT[j].middle_x <= element_x2[i] && placed_ELEMENT[j] == false)		//如果該元件的中心點在線的左邊，且還沒有x(未被放置)
			{
				ELEMENT_2D[j].sequence = ELEMENT[j].sequence;
				ELEMENT_2D[j].x = coordinate_x;
				ELEMENT_2D[j].word = ELEMENT[j].word;
				placed_ELEMENT[j] = true;						//已放置
				have_element = true;
			}
		if (have_element == true)
			coordinate_x++;
	}
		
	int coordinate_y = 1;
	for (int i = 0; i < ELEMENT.size() + 5; i++)
		placed_ELEMENT[i] = false;
	for (int i = 0; i < element_y2.size(); i++)					//水平線
	{
		bool have_element = false;
		for (int j = 0; j < ELEMENT.size(); j++)
			if (ELEMENT[j].middle_y <= element_y2[i] && placed_ELEMENT[j] == false)		//如果該元件的中心點在線的上面，且還沒有y(未被放置)
			{
				ELEMENT_2D[j].y = coordinate_y;
				placed_ELEMENT[j] = true;
				have_element = true;
			}
		if (have_element == true)
			coordinate_y++;
	}

	for (int i = 0; i < ELEMENT_2D.size(); i++)
		output_file << ELEMENT_2D[i].sequence << "@" << ELEMENT_2D[i].x << "@" << ELEMENT_2D[i].y << "@" << ELEMENT_2D[i].word << endl;

	file.close();
	output_file.close();
}

