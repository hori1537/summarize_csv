#coding: UTF-8


import os
import struct
from sys import exit
import csv
import numpy
import numpy as np

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

# tkinter ファイルダイアログを開き、GUIで操作できるライブラリ
#tkinter.Tk()のメソッド自体をtkという変数名に入れる tkでもtk_でもtk1などなんでも構わない
tk = tkinter.Tk()

# tk.withdraw withdraw：すなわち描画。　ファイルダイアログを表示する
# tk = tkinter.Tk()なので、 tkinter.Tk().withdrowと同義
tk.withdraw()

# currentdirectoryという変数に現在のカレントディレクトリをいれる
# ライブラリosのgetcwdというメソッドを使う。　get working directoryの略　作業中のディレクトリのパスを保存
# currentdirectoryの中身にたとえば'C:\Users\1310202\Desktop'がはいる

currentdirectory = os.getcwd()

print('csvファイルを選んでください')
sleep(0.3)


#csvfile_pathという変数に  でユーザーに選択させたCSVファイルのパスを保存する
# tkinterというライブラリの filedialog.askopenfilenameを使う
# ask open filename そのままの意味　開くファイル名をユーザーに尋ねる

# initialdir ファイル選択画面の初期フォルダ。　ここでは先ほど取得したcurrentdirectoryとしている
# title:ダイアログに出てくるメッセージ。省略可能

# filetypes 選択可能なファイルの拡張子を決める　 [('csv File', '*.csv')])
# 前半のcsv file はメッセージ　後半の*.csvが選択可能なファイルになる
# 仮にすべて選択可能にしたい場合は　 [('なんでもOK', '*.*')])などとすれば良い 

csvfile_path  = tkinter.filedialog.askopenfilename(initialdir = currentdirectory, 
title = 'csvファイルを１つ選択してください。　同フォルダ内のすべてのcsvファイルを変換します。', filetypes = [('csv File', '*.csv')])

# csvfile_path の中身：'C:\Users\1310202\Desktop\CSV\2019-03-05_19-47-02__19030501__PD.csv'

# csvfolder_pathという変数にcsvfile_pathのフォルダ名を入れる
csvfolder_path = os.path.dirname(csvfile_path)
# csvfile_path の中身：'C:\Users\1310202\Desktop\CSV'


#os.chdir change directoryの略　フォルダを移動する
#例：C:\Users\1310202\Desktop からC:\Users\1310202\Desktop\CSVへ移った
os.chdir(csvfolder_path)



#　上で選んだファイルと同じフォルダ内のすべてのファイルを処理することが目的
#　osライブラリのwalkというメソッドを使う

# walkメソッドで取得できるのは0:現在のディレクトリ名（フォルダ名）1:存在するフォルダ名　2:存在するファイル名
# 今回必要なのは、2:存在するファイル名
# よってos.walk(csvfolder_path).__next__()[2]となる
# __next__の説明は難しいので省略　またpython2ではnextという名前だったので、exceptに記載

# filelistの中身が['test1.csv', 'test2.csv', 'test3.csv', 'readme.txt']というリストになる


# refer https://www.sejuku.net/blog/63816

try:
    # python3 では__next__
    filelist = os.walk(csvfolder_path).__next__()[2]
    #print(filelist)
        
except:
    # 昔のpython2 では__next__ではなく、nextというメソッド名だった
    filelist = os.walk(csvfolder_path).next()[2]



#拡張子が.csvであるファイルを抽出
#python特有の内包表記を利用。ちょっと難しい

#filelistには['test1.csv', 'test2.csv', 'test3.csv', 'readme.txt']が含まれている

# os.path.splitext
#         split:分割   extinsion:拡張子の略 splittextではないので注意

# os.path.splitext('test1.csv')の戻り値は['test1', '.csv']のリストとなる
# os.path.splitext('test1.csv')[0]の戻り値は'test1'の文字列となる
# os.path.splitext('test1.csv')[1]の戻り値は'csv'の文字列となる


# os.path.splitext(i)の[1] が.csvかどうかで場合分けしている　

# 拡張子が大文字の場合もありうるので str.lower()で小文字に変換する

# os.path.splitext(i)               →['test1', '.CSV']
# os.path.splitext(i)[1]            →'.CSV'
# str.lower(os.path.splitext(i)[1]) →'.csv'


#python特有の内包表記と呼ばれる記述方式
#1行ですっきり書け、動作も早い。ただし慣れるまではわかりにくい
#　if str.lower(os.path.splitext(i)[1]) =='.csv' の部分で「拡張子がCSVだったら」という場合分け
#　i for i in filelistの部分で「拡張子がCSVだったら」filelistの要素をfilelist_csvに入れる

filelist_csv = [i for i in filelist if str.lower(os.path.splitext(i)[1]) =='.csv']

#filelst_csvの中身は['test1.csv', 'test2.csv', 'test3.csv'] となる。

#print(filelist)

#print('filelist_csv')
#print(filelist_csv)


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

#まとめ用のデータ保存先としてdata_outputを空(初期化)にしておく

data_output_forpd = [] 
header_forpd = []

for csvfilename in filelist_csv:
    print(csvfilename)

    with open(csvfilename , "r") as f:
        
        #csvの中身をfという変数にいれる
        # f は　<_io.TextIOWrapper name='2019-03-05_19-47-02__19030501__PD.csv' mode='r' encoding='cp932'>というCSVファイルをどう読むかというオブジェクトであって、CSVのデータそのものではない
        
        #csvというライブラリのreaderというメソッドを使う
        reader = csv.reader(f)
        #readerは変数名
        # readerの中身も<_csv.reader object at 0x0000025FBA83F3F0> であってデータそのものではない
        
        
        csv_data    = []
        YAvg_data   = []
        
        #1行ずつCSVを上から読み込み、csv_dataに書き込んでいく

        #csv_string=[line.rstrip().split(",") for line in open(csvfilename).readlines()]
        
        for row in reader:
            #print(row)
            #row = row.split()
            row = np.array(row)
            #print(row)
            
            csv_data.append(np.array(row))
            
        
        #print(csv_data)
        csv_data = np.array(csv_data)
        

        
        #csv_dataの中身がようやくcsvの行列データになった
        # 例:[[0,0,1],[0,1,0],[0,0,0]]
        
        #SR-5000のCSVファイルは測定データが保存されている行がファイルごとに異なる。
        #例１では28列目から始まっているが例２では26列目から始まっている
        #終列も同様にファイルごとに異なる
        
        #1列目の[Measurement]の2行下から測定データ。[Spectra]の1行上が終行
        
        #[Measurement]と[Spectra]をそれぞれ検索すればよい
        
        #以前の検索結果をクリアするために row_mes =''　row_spec=''　として空白を代入している。
        
        row_mes = ''
        row_spec = ''
        
        #enumerate 関数　便利
        # ここ読め　https://note.nkmk.me/python-enumerate-start/
        
        for index, data in enumerate(csv_data):
            if len(data) != 0:
                if data[0] == '[Measurement]':
                    row_mes = index
                    
                if data[0] == '[Spectral]':
                    row_spec = index
                    
        #測定データは[Measurement]の2行下から[Spectra]の1行上
        
        mes_data = csv_data[row_mes + 2 :row_spec]
        
        #測定点のデータ 1列目（x[0]）
        Point_data = [x[0] for x in mes_data]
        #YAvg_dataのデータ 1列目（x[4]）        
        YAvg_data  = [x[3] for x in mes_data]

        #出力用の変数data_outputにPoint_dataとYAvg_dataをextend (appendではない)
        data_output_forpd.extend([Point_data])
        data_output_forpd.extend([YAvg_data])
        
        #列名を追加
        header_forpd.append('Measure point')
        header_forpd.append(csvfilename)
        
        

#pandasのdataframeを用い、CSV出力に備える
df_ = pd.DataFrame(data_output_forpd)

#df_ の行列を転置（元のデータは横方向にデータが並ぶので、縦方向へと入れ替える）
# https://note.nkmk.me/python-pandas-t-transpose/
df_T  =df_.T

#de_Tのheader　列の名前を指定
# https://note.nkmk.me/python-pandas-dataframe-rename/
df_T.columns = header_forpd


#ファイルの保存されていた元フォルダの名前をCSVの名前とする
# https://note.nkmk.me/python-os-basename-dirname-split-splitext/
subdirname =os.path.basename(os.path.dirname(csvfile_path))

#データを書き出す
# https://note.nkmk.me/python-pandas-to-csv/
df_T.to_csv('data/' + str(subdirname)  + '_summerize.csv')


print('data/' + str(subdirname)  + '_summerize.csv')
print('csvファイルへの変換を完了しました。')
sleep(1)

