import re

def formatOutput(input_file):
	output_file = '1-2.txt'
	index = 1
	ifile = open(input_file, "r", encoding='utf-8')
	ofile = open(output_file, "w", encoding='utf-8')
	for line in ifile.readlines():
		rect_pattern = r"(Rect: )\(((-*\d+,){3}-*\d+)\)"
		name_pattern = r"((Name: )('([^']*)'))";
		value_pattern = r"((ValuePattern.Value: )('([^']*)'))";
		pass_pattern = r"(CustomControl|MenuBarControl|MenuItemControl|ListControl|Minimise|Close|Maximise)";
		rect_match = re.search(rect_pattern, line)
		name_match = re.search(name_pattern, line)
		value_match = re.search(value_pattern, line)
		pass_match = re.search(pass_pattern, line)

		if pass_match:
			continue
		else:
			if rect_match:
				written_content = str(index) + '@' + rect_match.group(2)
				written_content = written_content.replace(',', '@')
			if value_match:
				written_content += value_match.group(3)
			elif name_match :
				written_content += name_match.group(3)
			written_content = written_content.replace('\'', '@')
			written_content = written_content[:-1]
			written_content+='\n'
			ofile.write(written_content)
			index+=1
	ifile.close()
	ofile.close()
				
if __name__ == '__main__':
	formatOutput('@AutomationLog.txt')
