#/usr/bin/python
#coding:utf-8


import os
import struct
from sys import exit
import csv
import numpy
#import numpy as np
import pandas as pd
import tkinter
import tkinter.filedialog
from time import sleep

print('csvファイルをcsvに一括変換します')
sleep(0.5)
print('csvファイルはdataフォルダに保存されます')
sleep(0.5)
print('　')



#######################################################################################

tk = tkinter.Tk()
tk.withdraw()
currentdirectory = os.getcwd()

#print('csvファイルを選んでください')
sleep(0.3)

csvfile_path  = tkinter.filedialog.askopenfilename(initialdir = currentdirectory, 
title = 'csvファイルを１つ選択してください。　同フォルダ内のすべてのcsvファイルを変換します。', filetypes = [('csv File', '*.csv')])
csvfolder_path = os.path.dirname(csvfile_path)
os.chdir(csvfolder_path)

try:
    filelist = os.walk(csvfolder_path).__next__()[2]
except:
    filelist = os.walk(csvfolder_path).next()[2]

#拡張子が.csvであるファイルを抽出
filelist_csv = [os.path for i in filelist if os.path.splitext(i)[1]=='.csv']

#print(filelist)
#print(filelist_csv)
csvfilename = filelist[0]

data_output = []

######################################################################################
# データを格納するフォルダを作成する
if os.path.exists("data") == False:
    try:
        os.mkdir("data")
        print("dataフォルダを作成しました")
    except:
        print("dataフォルダの作成に失敗しました")
else:
        print("dataフォルダはすでに存在しています")

for csvfilename in filelist:
    #print(csvfilename)
    if "csv" in str(csvfilename):
        #print('csvです')
        with open(csvfilename , "r") as f:
            # xの開始、終端、ステップをヘッダーから取得する。
            #print("csvfilename: " , csvfilename)
            reader = csv.reader(f)
            
            csv_data = []
            for row in reader:
                csv_data.append(row)
            
            #print(csv_data)
            
            X_ = csv_data[3][1]
            Y_ = csv_data[3][2]
            Z_ = csv_data[3][3]
            x_ = csv_data[3][4]
            y_ = csv_data[3][5]
            z_ = csv_data[3][6]
            L_ = csv_data[3][10]
            a_ = csv_data[3][11]
            b_ = csv_data[3][12]
            #print('L_ is ', L_)
            #print('a_ is ', a_)
            #print('b_ is ', b_)

            data_output.append([csvfilename, X_, Y_, Z_, x_, y_, z_, L_, a_, b_])
    else:
        pass
        #print('gcm')
    print('output', data_output)
    header_csv  = ['filename', 'X', 'Y', 'Z', 'x', 'y', 'z', 'L*', 'a*', 'b*']

#データを書き出す
with open (file ='data/' + 'test.csv', mode = 'w', newline='') as exported_data_obj:
    writer_csv = csv.writer(exported_data_obj)
    writer_csv.writerow(header_csv)
    writer_csv.writerows(data_output)


print('csvファイルへの変換を完了しました。')
sleep(1)