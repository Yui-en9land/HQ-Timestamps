# キャラセレクト画面⇒ローディング画面⇒暗転でタイムスタンプを生成
# キャラセレクト画面で最後に一致した名前のファイルで使用キャラを判別
import cv2
import sys
import os
import numpy as np
import PySimpleGUI as sg
from tkinter import filedialog
import pyautogui

rrate = 3

import PySimpleGUI as sg

sg.theme('Dark Red')

BAR_MAX = 100

#　レイアウト（1段目：テキスト、2段目：プログレスバー、3段目：ボタン）
layout = [[sg.Text('　Hellish quart timestamp　')],
          [sg.ProgressBar(BAR_MAX, orientation='h', size=(20,20), key='-PROG-')],
          [sg.Cancel()]]

#　ウィンドウの生成
window = sg.Window('　Hellish Quartのタイムスタンプ生成　', layout)

# マッチングする座標の範囲（左上と右下の座標）
match_area_tl0 = (116, 10)  # 左上の座標
match_area_br0 = (126, 20)  # 右下の座標
match_area_tl = (30, 25)  # 左上の座標
match_area_br = (150, 50)  # 右下の座標
match2_area_tl = (500, 25)  # 左上の座標
match2_area_br = (620, 50)  # 右下の座標

# 画像ファイルがあるディレクトリのパス
image_dir_path1 = "name1"
image_dir_path2 = "name2"

# 画像ファイルの拡張子
extension = ".png"

name_chara = ['Alexander','Barabasz','Gedeon','Isabella','Jacek','Jan','Kalkstein','Laszlo','Marie','Marta','Samuel','Tarnavsky','Yendrek','Zera']
name_chara2 = ['Alexander','Barabasz','Gedeon','Isabella','Jacek','Jacek','Kalkstein','Laszlo','Marie','Marta','Samuel','Tarnavsky','Yendrek','Zera']

# 画像ファイルのリストを格納する配列
name_image = []
name_image2 = []

# 1playerのキャラ名前画像ファイルを読み込んでCV2グレーカラーにし配列に格納
for filename in os.listdir(image_dir_path1):
    if filename.endswith(extension):
        image_path = os.path.join(image_dir_path1, filename)
        image = cv2.imread(image_path)
        if image is not None:
            resized_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            name_image.append(resized_image)
# 2playerのキャラ名前画像ファイルを読み込んでCV2グレーカラーにし配列に格納
for filename in os.listdir(image_dir_path2):
    if filename.endswith(extension):
        image_path = os.path.join(image_dir_path2, filename)
        image = cv2.imread(image_path)
        if image is not None:
            resized_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            name_image2.append(resized_image)

# 検出する画像の読み込み
template_image = cv2.imread('timestamp.png',0)
template_image2 = cv2.imread('timestamp2.png',0)
template_image3 = cv2.imread('charaselect.png',0)

# ファイル選択ダイアログを表示
file_path = filedialog.askopenfilename(title="動画ファイルを選択")
# 動画ファイルを開く
cap = cv2.VideoCapture(file_path)

# 動画の解像度を取得
#width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 1/3にリサイズ
#new_width = width // rrate
#new_height = height // rrate

# 動画のリサイズ後の解像度を設定
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)

def check_color(frame, x, y, target_color, threshold=20):
    # フレームから指定された座標のピクセルの色を取得
    pixel_color = frame[y, x]

    # 指定した色との差の絶対値を計算
    color_diff = abs(int(pixel_color[0]) - target_color[0]) + \
                 abs(int(pixel_color[1]) - target_color[1]) + \
                 abs(int(pixel_color[2]) - target_color[2])

    # 差がしきい値以下であればTrueを返す
    if color_diff < threshold:
        return True
    else:
        return False

# 動画の総フレーム数を取得
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# 一致する時間のタイムスタンプを保存するリスト
timestamps = []
target_color = (3, 0, 209)
# 検出する座標
target_x = 121
target_y = 15
# しきい値 (色の許容範囲)
threshold = 50
player1_name = 'none'
player2_name = 'none'

frame_number = 1
x = 0
check_flag0 = 0
check_flag = 0
check_flag2 = 0
match_no = 1

start_comment = 'Timestamps:\n0:00:00 Settings\n'
timestamps.append(start_comment)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # フレームごとに画像の一致を検出
    if frame_number % 60 == 0:
        # リサイズ
        frame_r = cv2.resize(frame, (640, 360))
        frame_g = cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY)
        # フラッグの判定が終わっているか？
        if check_flag0 == 0:
#            cv2.imwrite('flag5.png',frame_r[match_area_tl0[1]:match_area_br0[1], match_area_tl0[0]:match_area_br0[0]])
#            cv2.imwrite('flag4.png',frame_r[match_area_tl0[1]:match_area_br0[1], match_area_tl0[0]-21:match_area_br0[0]-21])
#            cv2.imwrite('flag3.png',frame_r[match_area_tl0[1]:match_area_br0[1], match_area_tl0[0]-43:match_area_br0[0]-43])
#            cv2.imwrite('flag2.png',frame_r[match_area_tl0[1]:match_area_br0[1], match_area_tl0[0]-65:match_area_br0[0]-65])
#            cv2.imwrite('flag1.png',frame_r[match_area_tl0[1]:match_area_br0[1], match_area_tl0[0]-87:match_area_br0[0]-87])
#            cv2.imwrite('flag12.png',frame_r[match_area_tl0[1]:match_area_br0[1], match_area_tl0[0]+489:match_area_br0[0]+489])
#            cv2.imwrite('flag22.png',frame_r[match_area_tl0[1]:match_area_br0[1], match_area_tl0[0]+489-21:match_area_br0[0]+489-21])
#            cv2.imwrite('flag32.png',frame_r[match_area_tl0[1]:match_area_br0[1], match_area_tl0[0]+489-43:match_area_br0[0]+489-43])
#            cv2.imwrite('flag42.png',frame_r[match_area_tl0[1]:match_area_br0[1], match_area_tl0[0]+489-65:match_area_br0[0]+489-65])
#            cv2.imwrite('flag52.png',frame_r[match_area_tl0[1]:match_area_br0[1], match_area_tl0[0]+489-87:match_area_br0[0]+489-87])
            # 1P側の5番目のフラッグの色を確認
            if check_color(frame_r, target_x, target_y, target_color, threshold):
                check_flag0 = 1
                if check_color(frame_r, target_x + 489 - 65, target_y, target_color, threshold):
                    winner = 'Player1 win by 5:4\n'
                elif check_color(frame_r, target_x + 489 - 43, target_y, target_color, threshold):
                    winner = 'Player1 win by 5:3\n'
                elif check_color(frame_r, target_x + 489 - 21, target_y, target_color, threshold):
                    winner = 'Player1 win by 5:2\n'
                elif check_color(frame_r, target_x + 489, target_y, target_color, threshold):
                    winner = 'Player1 win by 5:1\n'
                else:
                    winner = 'Player1 win by 5:0\n'
                timestamps.append(winner)
                print(winner)
                match_no += 1
            if check_color(frame_r, target_x+489-87, target_y, target_color, threshold):
                check_flag0 = 1
                if check_color(frame_r, target_x - 21, target_y, target_color, threshold):
                    winner = 'Player2 win by 4:5\n'
                elif check_color(frame_r, target_x - 43, target_y, target_color, threshold):
                    winner = 'Player2 win by 3:5\n'
                elif check_color(frame_r, target_x - 65, target_y, target_color, threshold):
                    winner = 'Player2 win by 2:5\n'
                elif check_color(frame_r, target_x - 87, target_y, target_color, threshold):
                    winner = 'Player2 win by 1:5\n'
                else:
                    winner = 'Player2 win by 0:5\n'
                timestamps.append(winner)
                print(winner)
                match_no += 1


        #            if pyautogui.pixelMatchesColor(204, 69, (232, 222, 213)):
            # 2P側の5番目のフラッグの色を確認
#            if pyautogui.pixelMatchesColor(204, 69, (232, 222, 213)):

        # キャラセレクト画面を判定しているか？
        if check_flag == 0:
            # キャラセレクト画面を判定
            result1 = cv2.matchTemplate(frame_g, template_image3, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result1)
            # 閾値を設定して一致があった場合にタイムスタンプを保存
            if max_val > 0.7:
#                cv2.imwrite('test1.png',frame_g)
                check_flag = 1
                print('キャラクターセレクト画面を判定')
    if (check_flag2 == 0) and (check_flag == 1) and (check_flag2 == 0):
        if frame_number % 15 == 0:
            frame_r = cv2.resize(frame, (640, 360))
            frame_g = cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY)
            match_area = frame_g[match_area_tl[1]:match_area_br[1], match_area_tl[0]:match_area_br[0]]
            max_temp = 0
            # 1プレイヤー側のキャラの名前を判別
            for name_index, image in enumerate(name_image):
                result_name = cv2.matchTemplate(match_area, image, cv2.TM_CCOEFF_NORMED)
                min_val, max_val2, min_loc, max_loc = cv2.minMaxLoc(result_name)
                if max_val2 > 0.8:
                    if max_temp < max_val2:
#                        cv2.imwrite('test1_1.png', match_area)
                        player1_name = name_chara[name_index]
#                        cv2.imwrite('name0/hq1_' + player1_name + '.png', match_area)
                        max_temp = max_val2
#                    print(' pl1:')
#                    print(player1_name)
            match_area = frame_g[match2_area_tl[1]:match2_area_br[1], match2_area_tl[0]:match2_area_br[0]]
            max_temp = 0
            # 2プレイヤー側のキャラの名前を判別
            for name_index2, image2 in enumerate(name_image2):
                result_name2 = cv2.matchTemplate(match_area, image2, cv2.TM_CCOEFF_NORMED)
                min_val, max_val2, min_loc, max_loc = cv2.minMaxLoc(result_name2)
                if max_temp < max_val2:
                    if max_val2 > 0.8:
#                        cv2.imwrite('test2_1.png', match_area)
#                        print(f'pl2:max={max_val2} index={name_index2} name={name_chara2[name_index2]}')
                        player2_name = name_chara2[name_index2]
#                        cv2.imwrite('name0/hq2_' + player2_name + '.png', match_area)
                        max_temp = max_val2
#                        print(' pl2:')
#                        print(player2_name)

            result2 = cv2.matchTemplate(frame_g, template_image2, cv2.TM_CCOEFF_NORMED)
            min_val, max_val2, min_loc, max_loc = cv2.minMaxLoc(result2)
            # 閾値を設定して一致があった場合にタイムスタンプを保存
            if max_val2 > 0.65:
#                cv2.imwrite('test2.png',frame_g)
                check_flag2 = 1
                x = 0
                print(' ロード画面を判定')

        # 閾値を設定して一致があった場合にタイムスタンプを保存
    if (check_flag == 1) and (check_flag2 == 1):
        if frame_number % 60 == 0:
    #           cv2.imwrite('tmp.png', template_image)
#           cv2.imwrite('test3.png', frame_g)
            image_diff = cv2.absdiff(template_image, frame_g)
            similarity = 1 - (image_diff.mean() / 255.0)
#            result3 = cv2.matchTemplate(frame_g, template_image, cv2.TM_CCOEFF_NORMED)
#            min_val, max_val3, min_loc, max_loc = cv2.minMaxLoc(result3)

#            if max_val3 > 0.9:
            if similarity > 0.95 :
#                cv2.imwrite('tmp.png',template_image)
#                cv2.imwrite('test3.png',frame_g)
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                time_in_seconds = frame_number / fps
                # 時間、分、秒の計算
                hours = int(time_in_seconds) // 3600
                minutes = (int(time_in_seconds) % 3600) // 60
                seconds = int(time_in_seconds) % 60
                # フォーマットされた文字列を作成
                timestamp = "{:01d}:{:02d}:{:02d} M{:02d}: Player1 - {} vs Player2 - {}\n".format(hours, minutes, seconds,match_no,player1_name,player2_name)
                timestamps.append(timestamp)
                print(timestamp)
                check_flag = 0
                check_flag2 = 0
                check_flag0 = 0
                player1_name = 'none'
                player2_name = 'none'

    progress = (frame_number / frame_count) * 100
    sys.stdout.write(f'\r進捗: {progress:.2f}% ')
    frame_number += 1
    #　入力待ち（10msでタイムアウトして、次の処理へ進む）
    event, values = window.read(timeout=1)

    #　キャンセルボタンか、ウィンドウの右上の×が押された場合の処理
    if event == 'Cancel' or event == sg.WIN_CLOSED:
        break

    #　プログレスバーの表示更新（カウンタ(i)をインクリメントして表示）
    window['-PROG-'].update(progress)

# 動画ファイルを閉じる
cap.release()

# ファイルが存在する場合は削除
if os.path.exists('timestamps.txt'):
    os.remove('timestamps.txt')
# タイムスタンプをファイルに一括で書き込む
with open('timestamps.txt', 'a') as file:
    for timestamp in timestamps:
        file.write(timestamp)

# 進捗情報の改行
print('\n解析完了')
print('タイムスタンプをファイルに書き込みました')
window.close()

