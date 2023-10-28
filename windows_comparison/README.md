2023/08/12

現在可以不用到windows_comparision_model.py、windows_comparision_examinee.py這兩個檔案改Window_Name

只需要在cmd中輸入"python windows_comparision_model.py 要讀取的視窗名稱(不加.exe)"

直接點也可以用，但預設讀取視窗是CardGame

-------------------------------

2023/09/25

更新馮定安的程式，並修改原本的程式

新增UI

-------------------------------

2023/10/4

更新視窗名稱判斷

UI新增查看原始圖像的功能

新增Xclean.py，方便刪除中間檔案，執行完UI後就可以考慮使用

-------------------------------

2023/10/9

更新定安的程式CaptureWindowInfo.py

更新佳揚的程式(有問題)

新增UI介面的背景圖

-------------------------------

2023/10/10

更新佳揚的程式

新增說明文件

修復UI運行問題

-------------------------------

2023/10/16

更新TwoDIndexTransformation_for_examinee.py，在此階段(二)若匹配的元件數小於一半，則不運行後續階段

更新UI介面的效率，現在直接在主頁面運行的效率變快，跟直接運行windows_comparison_model.py、
windows_comparison_examinee.py的效率差不多，直接在主頁面運行程式就好

更新Xclean.py，現在會刪除所有需要刪除的檔案

-------------------------------

2023/10/26

更新DirectionMethod(2D_LCS).py，現在是4個規則都會各跑一次，將結果輸出到statistics.txt中。

CaptureWindowInfo.py需要修正。

-------------------------------

2023/10/27

更新TwoDIndexTransformation_for_examinee.py，現在相同文字的元件順序先依照x座標的大小排序，再依照y座標的大小排序(小到大)。

結果顯示圖片若有同文字元件會有問題，需要修改。

-------------------------------

2023/10/28

更新TwoDIndexTransformation_for_model.py，現在相同文字的元件順序先依照x座標的大小排序，再依照y座標的大小排序(小到大)。

更新TwoDIndexTransformation_for_model.py、TwoDIndexTransformation_for_examinee.py、DirectionMethod(2D_LCS).py、DrawTable_model.py、DrawTable_examinee.py、MarkOriginalImage.py的輸出，包含文字輸出及圖片輸出。現在考生視窗的結果顯示圖片基本上沒有問題，但標準視窗的結果顯示圖片在有"同文字元件"的情況下會出問題，原因是2D LCS目前只能得到考生視窗中正確元件的二維轉換座標，無法得到標準視窗中正確元件的二維轉換座標，使得無法精確判斷標準視窗中正確的元件。
