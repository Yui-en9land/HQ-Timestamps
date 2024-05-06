Hellish Quartの対戦動画(NHK)のタイムスタンプを作るアプリです。

　
■制約
　16：9の動画にのみ対応しています。

■使い方
 1.timestamp.exe
　アプリ(timestamp.exe)を起動
  対戦動画を選択
　終了すると同フォルダにtimestamp.txtが生成されます。
　CANCELで中断した場合も同様に途中までのtimestampがtxtに生成されます。

 2.rename.exe(timestamps.txtの名前をリネームするためのソフトです)
  リネームファイル(players.txt)を用意
　⇒1P側と2P側のプレイヤー名をスペース区切りで記載してください(sample参照）
　1で作成したタイムスタンプのファイル(timestamps.txt)を用意
　アプリ(rename.exe)を起動
　timestamps_rename.txtが生成されます。
　※ファイル名は固定ですので別の名称ですと動作しません。

■注意事項
　添付画像は検出に用いてますので削除、変更しないでください。
　稀に誤って検出するため目視で確認をお願いします。
　検出方法は　キャラ選択画面→ローディング画面→暗転で検出していますので
　動画内で同様の手順を踏んでいると誤検出してしまいます。


■変更履歴
2023-10-16　新規作成
2023-10-20　検出方法に誤りがあったため修正
2023-10-22  16：9の解像度ならどの解像度でも対応
2023-11-11  誤検出対策
2024-05-04  使用キャラの認識と勝敗のフラッグ数の認識に対応
　　　　　　キャラクターが増えたため選択画面を更新
　　　　　　timestampのテキストファイルがすでにある場合は削除して新規に作成するよう変更
2024-05-05  使用キャラが見つからない場合にエラーで止まらないよう修正
　　　　　　キャラの認識の閾値を下げました
2024-05-06  キャラ認識用の画像ファイルを更新
　　　　　　Youtube用のコメントのフォーマットの先頭に「Timestamps:」と「0:00:00 Settings」を追加
　　　　　　Youtube用のコメントのフォーマットに不備があったため修正
　　　　　　キャラのスペルが間違っていたので修正