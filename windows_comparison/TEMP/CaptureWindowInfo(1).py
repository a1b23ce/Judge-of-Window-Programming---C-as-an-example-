import sys
import time
import os
import subprocess
import re
import time
import uiautomation as auto

# 資料夾名稱
folder_path = None

windows = []
execs = []
target_windows = []
exec_pattern = r".*\.exe"
wdInfo = open("1-2.txt", 'w', encoding='utf-8')

def getExecFileName():
    file_names = os.listdir(folder_path)
#    for str in file_names:
#	    if re.search(exec_pattern, str):
#		    print(str)
    for str in file_names:
        if re.search(exec_pattern, str):
            return os.path.join(folder_path, str)

def collectName():
    control = auto.GetRootControl()
    for c, d in auto.WalkControl(control, True, 1):
        # print(repr(c.Name))
        windows.append(repr(c.Name))

def getTargetWindowName():
    target_prog = getExecFileName()
    control = auto.GetRootControl()
    proc = subprocess.Popen(target_prog)
    for sleep_time in range(1, 20):
        time.sleep(1)
        for c, d in auto.WalkControl(control, True, 1):
            cur_name = repr(c.Name)
            if not isExist(cur_name):
                return cur_name.replace('\'', ''), proc
        sleep_time+=1

def isExist(cur_name):
    for wd in windows:
        if cur_name == wd:
            return True
    return False

def getWinData():
    pic_folder_path = folder_path + '/window_screenshot.png'
    wdName, proc = getTargetWindowName()
    control = auto.WindowControl(searchDepth=1, Name=wdName)
    control.CaptureToImage(pic_folder_path)
    i = 1
    for c, d in auto.WalkControl(control, True, 0xFFFFFFFF):
        i = getControlInfo(c, i)
    wdInfo.close()
    proc.terminate()

def getControlInfo(control: auto.Control, i: int):
    wddata = repr(control.BoundingRectangle)
    wddata = repr(i)+'@'+re.sub(r'Rect|\(|\)|\[.*?\]', '', wddata.replace(',', '@'))
    supportedPatterns = list(filter(lambda t: t[0], ((control.GetPattern(id_), name) for id_, name in auto.PatternIdNames.items())))
    for pt, name in supportedPatterns:
        # print(name)
        if isinstance(pt, auto.ValuePattern) :
            wddata+=(repr(pt.Value).replace('\'', '@')[:-1])
            valueWritten = True
        else:
            valueWritten = False
    isLegitName = not re.search(r'ButtonControl|ThumbControl|Header|CustomControl|TableControl|PaneControl|WindowControl|TitleBarControl', repr(control.ControlTypeName))\
                and not re.search(r'Close|Maximise|Minimise|System', repr(control.Name))
    if not valueWritten and isLegitName:
        wddata+=(repr(control.Name).replace('\'', '@')[:-1])
        nameWritten = True
    else:
        nameWritten = False
    if (nameWritten or valueWritten) and re.search(r'(\d+@){5}.+', wddata):
        wdInfo.write(wddata + '\n')
        # print(repr(control.ControlTypeName))
        # print(wddata)
        return i+1
    else:
        return i

def get_argument():
	if len(sys.argv) < 2:
		return None
	return sys.argv[1]

def main():
    global folder_path
    folder_path = get_argument()
    if folder_path is None:
        folder_path = 'model'
	
    collectName()
    getExecFileName()
    getWinData()


if __name__ == '__main__':
    main()
