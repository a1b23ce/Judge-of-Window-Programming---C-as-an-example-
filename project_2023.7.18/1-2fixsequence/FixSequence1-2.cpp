嚜?include "FixSequence1-2.h"

bool isInteger(const std::string& s)
{
	try
	{
		size_t pos = 0;
		std::stoi(s, &pos);
		return pos == s.length(); // 蝣箔??游?銝脤頧??箸??
	}
	catch (const std::exception& e)
	{
		return false; // 頧?憭望?嚗??舀??
	}
}

bool isFloat(const std::string& s)
{
	try
	{
		size_t pos = 0;
		std::stof(s, &pos);
		return pos == s.length(); // 蝣箔??游?銝脤頧??箸筑暺
	}
	catch (const std::exception& e)
	{
		return false; // 頧?憭望?嚗??舀筑暺
	}
}

void FixSeq()
{
	vector <element> ELEMENT;
	vector <element> ELEMENT2;
	vector <element> ELEMENT3;
	vector <string> elements;
	string temp_line;

	ifstream file(inputfile_path);			//read file
	if (!file.is_open())
	{
		cout << "?⊥???瑼?嚗? << inputfile_path << endl;
		return;
	}
	ifstream file2(inputfile_path2);			//read file
	if (!file.is_open())
	{
		cout << "?⊥???瑼?嚗? << inputfile_path2 << endl;
		return;
	}

	ofstream output_file(outputfile_path);	//write file

	while (getline(file, temp_line))
	{
		elements.clear();

		stringstream ss(temp_line);
		string item;
		int item_number = 0;
		while (getline(ss, item, '@'))		//隞世蝚西????辣
		{
			elements.push_back(item);
			item_number++;
		}

		if (item_number == 6)				//靽璈
		{
			if (isInteger(elements[0]) && isFloat(elements[1]) && isFloat(elements[2]) && isFloat(elements[3]) && isFloat(elements[4]))
			{
				ELEMENT.push_back(element(atoi(elements[0].c_str()), stof(elements[1]), stof(elements[2]), stof(elements[3]), stof(elements[4]), elements[5]));
			}
		}
	}

	while (getline(file2, temp_line))
	{
		elements.clear();

		stringstream ss(temp_line);
		string item;
		int item_number = 0;
		while (getline(ss, item, '@'))		//隞世蝚西????辣
		{
			elements.push_back(item);
			item_number++;
		}

		if (item_number == 6)				//靽璈
		{
			if (isInteger(elements[0]) && isFloat(elements[1]) && isFloat(elements[2]) && isFloat(elements[3]) && isFloat(elements[4]))
			{
				ELEMENT2.push_back(element(atoi(elements[0].c_str()), stof(elements[1]), stof(elements[2]), stof(elements[3]), stof(elements[4]), elements[5]));
			}
		}
	}

	bool* placed_ELEMENT2 = new bool[ELEMENT2.size() + 5];		//撌脫蝵??芣蝵?
	for (int i = 0; i < ELEMENT2.size() + 5; i++)
		placed_ELEMENT2[i] = false;

	for (int i = 0; i < ELEMENT.size(); i++)
	{
		for (int j = 0; j < ELEMENT2.size(); j++)
		{
			if (ELEMENT2[j].word == ELEMENT[i].word && placed_ELEMENT2[j] == false)
			{
				ELEMENT3.push_back(element(ELEMENT[i].index, ELEMENT2[j].x1, ELEMENT2[j].y1, ELEMENT2[j].x2, ELEMENT2[j].y2, ELEMENT2[j].word));
				placed_ELEMENT2[j] = true;
				break;
			}
		}
	}

	int element_num = ELEMENT2.size();
	for (int i = 0; i < ELEMENT2.size(); i++)
		if (placed_ELEMENT2[i] == false)
		{
			ELEMENT3.push_back(element(element_num, ELEMENT2[i].x1, ELEMENT2[i].y1, ELEMENT2[i].x2, ELEMENT2[i].y2, ELEMENT2[i].word));
			element_num++;
		}

	for (int i = 0; i < ELEMENT3.size(); i++)
	{
		output_file << ELEMENT3[i].index << "@" << ELEMENT3[i].x1 << "@" << ELEMENT3[i].y1 << "@" << ELEMENT3[i].x2 << "@" << ELEMENT3[i].y2 << "@" << ELEMENT3[i].word << endl;
	}

	file.close();
	file2.close();
	output_file.close();
}