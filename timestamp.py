# キャラセレクト画面⇒ローディング画面⇒暗転でタイムスタンプを生成
# キャラセレクト画面で最後に一致した名前のファイルで使用キャラを判別
import cv2
import sys
import os
import numpy as np
import PySimpleGUI as sg
from tkinter import filedialog
import pyautogui
import datetime

rrate = 3

import PySimpleGUI as sg

sg.theme('Dark Red')

BAR_MAX = 100
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
flag_flag = 0
chara_flag = 0
stage_flag = 0
load_flag = 0
black_flag = 0
init_check = 0
match_no = 1

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

#name_chara = ['Alexander', 'Barabasz', 'Gedeon', 'Isabella', 'Jacek', 'Jan', 'Kalkstein', 'Laszlo', 'Marie', 'Marta',
#              'Samuel', 'Tarnavsky', 'Yendrek', 'Zera']
name_chara = []
#name_chara2 = ['Alexander', 'Barabasz', 'Gedeon', 'Isabella', 'Jacek', 'Jacek', 'Kalkstein', 'Laszlo', 'Marie', 'Marta',
#               'Samuel', 'Tarnavsky', 'Yendrek', 'Zera']
name_chara2 = []

start_comment = 'Timestamps:\n0:00:00 Settings\n'
timestamps.append(start_comment)

# 　レイアウト（1段目：テキスト、2段目：プログレスバー、3段目：ボタン）
layout = [[sg.Text('　Hellish quart timestamp　')],
          [sg.ProgressBar(BAR_MAX, orientation='h', size=(20, 20), key='-PROG-')],
          [sg.Cancel()]]

# 　ウィンドウの生成
window = sg.Window('　Hellish Quartのタイムスタンプ生成　', layout)

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
    filename = filename.replace('hq1_','')
    filename = filename.replace('.png','')
    name_chara.append(filename)

# 2playerのキャラ名前画像ファイルを読み込んでCV2グレーカラーにし配列に格納
for filename in os.listdir(image_dir_path2):
    if filename.endswith(extension):
        image_path = os.path.join(image_dir_path2, filename)
        image = cv2.imread(image_path)
        if image is not None:
            resized_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            name_image2.append(resized_image)
    filename = filename.replace('hq2_','')
    filename = filename.replace('.png','')
    name_chara2.append(filename)

# 検出する画像の読み込み
black_image = cv2.imread('check/black.png', 1)
load_image = cv2.imread('check/load.png', 0)
chara_select = cv2.imread('check/charaselect.png', 0)
stage_select = cv2.imread('check/stageselect.png', 0)
# ファイル選択ダイアログを表示
file_path = filedialog.askopenfilename(title="動画ファイルを選択")
# 動画ファイルを開く
cap = cv2.VideoCapture(file_path)
fps = cap.get(cv2.CAP_PROP_FPS)


# 動画の解像度を取得
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 1/3にリサイズ
# new_width = width // rrate
# new_height = height // rrate

# 動画のリサイズ後の解像度を設定
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)

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


# フラッグの判別
def flag_check(frame_r, timestamps):
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
        # 5番目のフラッグが赤の時、右側からフラッグの色を判定
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
        flag_flag = 1

    elif check_color(frame_r, target_x + 489 - 87, target_y, target_color, threshold):
        # 5番目のフラッグが赤の時、左側からフラッグの色を判定
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
        flag_flag = 1
    else:
        flag_flag = 0
    return flag_flag


# キャラセレクト画面の判別
def chara_check(frame_g):
    # キャラセレクト画面を判定
    result1 = cv2.matchTemplate(frame_g, chara_select, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result1)
    # 閾値を設定して一致があった場合にタイムスタンプを保存
    if max_val > 0.7:
        # cv2.imwrite('test1.png',frame_g)
        print('キャラクターセレクト画面を判定')
        chara_flag = 1
    else:
        chara_flag = 0
    return chara_flag


# プレイヤーの使用するキャラクターの判別
def player_check(frame_g, player1_name, player2_name):
    match_area = frame_g[match_area_tl[1]:match_area_br[1], match_area_tl[0]:match_area_br[0]]
    max_temp = 0
    # 1プレイヤー側のキャラの名前を判別
    for name_index, image in enumerate(name_image):
        result_name = cv2.matchTemplate(match_area, image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val2, min_loc, max_loc = cv2.minMaxLoc(result_name)
        if max_val2 > 0.8:
            if max_temp < max_val2:
                player1_name = name_chara[name_index]
                max_temp = max_val2
                # cv2.imwrite('test1_1.png', match_area)
                # cv2.imwrite('name0/hq1_' + player1_name + '.png', match_area)
                # print(' pl1:')
                # print(player1_name)
    match_area = frame_g[match2_area_tl[1]:match2_area_br[1], match2_area_tl[0]:match2_area_br[0]]
    max_temp = 0
    # 2プレイヤー側のキャラの名前を判別
    for name_index2, image2 in enumerate(name_image2):
        result_name2 = cv2.matchTemplate(match_area, image2, cv2.TM_CCOEFF_NORMED)
        min_val, max_val2, min_loc, max_loc = cv2.minMaxLoc(result_name2)
        if max_temp < max_val2:
            if max_val2 > 0.8:
                player2_name = name_chara2[name_index2]
                max_temp = max_val2
                # cv2.imwrite('test2_1.png', match_area)
                # cv2.imwrite('name0/hq2_' + player2_name + '.png', match_area)
                # print(f'pl2:max={max_val2} index={name_index2} name={name_chara2[name_index2]}')
                # print(' pl2:')
                # print(player2_name)
                chara_flag = 1
    return player1_name, player2_name

# 暗転画面の判別
def black_check(frame_c):
    # cv2.imwrite('tmp.png', black_image)
    # cv2.imwrite('test3.png', frame_g)
    # result3 = cv2.matchTemplate(frame_c, black_image, cv2.TM_CCOEFF_NORMED)
    # min_val, max_val3, min_loc, max_loc = cv2.minMaxLoc(result3)
    # if max_val3 > 0.999:
    # 通常の比較だとロード画面と暗転が一致してしまうため、絶対値で比較
    # cv2.imwrite( 'black_tmp.png', black_image )
    # cv2.imwrite( 'black.png', frame_c )
    image_diff = cv2.absdiff(black_image, frame_c)
    similarity = 1 - (image_diff.mean() / 255.0)
    if similarity > 0.9:
        black_flag = 1
    else:
        black_flag = 0
    return black_flag


# 動画の総フレーム数を取得
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # フラッグ判定とキャラセレクト画面はフレームレートの２倍で判定
    if frame_number % (fps * 2) == 0:
        # 640*360(16:9)にリサイズ
        frame_r = cv2.resize(frame, (640, 360))
        # フラッグ未判定？
        if flag_flag == 0:
            # フラッグ判定
            flag_flag = flag_check(frame_r, timestamps)
            if flag_flag == 1:
                match_no += 1
        # フラッグの判定済または初回判定？　かつキャラセレクト画面未判定？
        # 試合途中から録画開始するパターンもあるためflag_flagの初期値を0に設定
        # そのため初回のみflag_flagが0でも動作するようinit_checkで初回のみ動作させる
        if (chara_flag == 0) and ((flag_flag == 1) or(init_check == 0)):
            # グレースケールに変更
            frame_g = cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY)
            # キャラセレクト画面判定
            chara_flag = chara_check(frame_g)
            # 判定後にメインメニューに戻った時に再度キャラセレクト判定ができるようにリセットする
            if chara_flag == 1:
                load_flag = 0
                init_check = 1

    # キャラセレクト画面判定済かつステージセレクト画面未判定
    if (stage_flag == 0) and (chara_flag == 1):
        # キャラセレクトとステージセレクトはシビアなため15FPSで判定
        if frame_number % 15 == 0:
            # 640*360(16:9)にリサイズ
            frame_r = cv2.resize(frame, (640, 360))
            # グレースケールに変更
            frame_g = cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY)
            # プレイヤーキャラセレクト判定(プレイヤーキャラセレクトは終了が判定できないためフラグは使用しない)
            [player1_name, player2_name] = player_check(frame_g, player1_name, player2_name)

            #ステージセレクト画面を判定
            result2 = cv2.matchTemplate(frame_g, stage_select, cv2.TM_CCOEFF_NORMED)
            min_val, max_val2, min_loc, max_loc = cv2.minMaxLoc(result2)
            cv2.imwrite('stageselect_.png', frame_g)
            if max_val2 > 0.6:
                stage_flag = 1
                x = 0
                print('ステージセレクト画面を判定')
                chara_flag = 0

    # ステージセレクト画面判定済かつLoad画面未判定
    if (load_flag == 0) and (stage_flag == 1):
        # ロード画面は長いのでフレームレートの２倍で判定
        if frame_number % (fps * 2) == 0:
            # 640*360(16:9)にリサイズ
            frame_r = cv2.resize(frame, (640, 360))
            # グレースケールに変更
            frame_g = cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY)
            result2 = cv2.matchTemplate(frame_g, load_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val2, min_loc, max_loc = cv2.minMaxLoc(result2)
            if max_val2 > 0.8:
                # cv2.imwrite('test2.png',frame_g)
                load_flag = 1
                x = 0
                print('ロード画面を判定')
                chara_flag = 0

    # 暗転未判定かつロード画面判定済
    if (black_flag == 0) and (load_flag == 1):
        # 暗転は長いのでフレームレ－トの２倍で判定
        if frame_number % (fps * 2) == 0:
            # 640*360(16:9)にリサイズ
            frame_r = cv2.resize(frame, (640, 360))
            # カラーに変更(グレースケールだと判別が難しいため)
            frame_c = cv2.cvtColor(frame_r, cv2.COLOR_BGR2RGB)
            black_flag = black_check(frame_c)
    # 暗転判定したらファイル出力
    if black_flag == 1:
        time_in_seconds: float = frame_number / fps
        # 時間、分、秒の計算
        hours = int(time_in_seconds) // 3600
        minutes = (int(time_in_seconds) % 3600) // 60
        seconds = int(time_in_seconds) % 60
        # フォーマットされた文字列を作成
        timestamp = "{:01d}:{:02d}:{:02d} M{:02d}: Player1 - {} vs Player2 - {}\n".format(hours, minutes, seconds,
                                                                                          match_no, player1_name,
                                                                                          player2_name)
        timestamps.append(timestamp)
        print("\n" + timestamp)
        load_flag = 0
        black_flag = 0
        chara_flag = 0
        flag_flag = 0
        stage_flag = 0
        player1_name = 'none'
        player2_name = 'none'

    # プログレスバーの更新とコンソール出力
    time_in_seconds: float = frame_number / fps
    # 時間、分、秒の計算
    hours = int(time_in_seconds) // 3600
    minutes = (int(time_in_seconds) % 3600) // 60
    seconds = int(time_in_seconds) % 60
    # フォーマットされた文字列を作成
    timestamp = "{:01d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    progress = (frame_number / frame_count) * 100
    sys.stdout.write(f'\r進捗: {progress:.2f}%({timestamp}) ')
    frame_number += 1

    # 　入力待ち（1msでタイムアウトして、次の処理へ進む）
    event, values = window.read(timeout=1)

    # 　キャンセルボタンか、ウィンドウの右上の×が押された場合の処理
    if event == 'Cancel' or event == sg.WIN_CLOSED:
        break

    # 　プログレスバーの表示更新（カウンタ(i)をインクリメントして表示）
    window['-PROG-'].update(progress)

# 動画ファイルを閉じる
cap.release()

d_today = datetime.date.today()
str_today = d_today.strftime('%Y%m%d')
# ファイルが存在する場合は削除
if os.path.exists(str_today + 'timestamps.txt'):
    os.remove(str_today + 'timestamps.txt')
# タイムスタンプをファイルに一括で書き込む
with open(str_today + 'timestamps.txt', 'a') as file:
    for timestamp in timestamps:
        file.write(timestamp)

# 進捗情報の改行
print('\n解析完了')
print('タイムスタンプをファイルに書き込みました')
window.close()
