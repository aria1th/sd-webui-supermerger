# SuperMerger
- Model merge extention for [AUTOMATIC1111's stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) 
- Merge models can be loaded directly for generation without saving

# Recent Update
すべての更新履歴は[こちら](https://github.com/hako-mikan/sd-webui-supermerger/blob/ver2/changelog.md)にあります。  
All updates can be found [here](https://github.com/hako-mikan/sd-webui-supermerger/blob/ver2/changelog.md).

### update to version 3 2023.02.17.2020(JST)
- LoRA関係の機能を追加しました
- Logを保存し、設定を呼び出せるようになりました
- safetensors,fp16形式での保存に対応しました
- weightのプリセットに対応しました
- XYプロットの予約が可能になりました
diffusersのインストールが必要になりました。windowsの場合はweb-uiのフォルダでコマンドプロンプトから"pip install diffusers"を打つことでインストールできる場合がありますが環境によります。
# 

日本語説明は[後半](#概要)後半にあります。

# Overview
This extension allows you to load a merged model for image generation without saving.
Until now, it was necessary to save the merged model and delete it if you did not like it, but by using this extension, you can prevent the consumption of HDD and SSD.

## Usage

### Merge mode
#### Weight sum
Normal merge. alpha is used. if MBW is enabled, MBW base is used as alpha.
#### Add difference
Difference merge, if MBW is enabled, MBW base is used as alpha
#### Triple sum
Merges 3 models at the same time. This function was added because there were three model selection windows, but I am not sure if it works effectively or not. if MBW is enabled, enter MBW parameters for alpha and beta.
#### sum Twice
Weight sum twice.

### merge
After merging, load the model as a generated model. __Note that a different model is loaded from the model information in the upper left corner.__ It will be reset when you re-select the model in the model selection screen in the upper left corner.


### gen
Generate images using the settings in the text2image tab.

### Merge and Gen
Merge and Generate image after merging

### Save merged model
Save the currently loaded merged model (merges a new one, because saving the loaded model saves it as a fp16 model). This is because saving the loaded model assumes it is a single-precision model.)

### Sequential XY Merge and Generation
Sequential merge image generation.
#### alpha,beta
Change alpha, beta.
#### seed
Change the seed. Assuming -1 will result in a fixed seed in the opposite axis direction.
#### model_A,B,C
Change model. The model selected in the model selection window is ignored.
#### pinpoint blocks
Change only specific blocks in MBW. Choose alpha or beta for the opposite axis. If you enter a block ID, only that block's alpha (beta) will change. Separate with commas like any other type. Multiple blocks can be changed at the same time by separating them with spaces or hyphens. Adding NOT at the beginning reverses the change target. If NOT IN09-OUT02 is set, all except IN09-OUT02 will change. NOT has no effect unless entered first.
##### Input example
IN01, OUT10 OUT11, OUT03-OUT06, OUT07-OUT11, NOT M00 OUT03-OUT06
in this case
- 1: Only IN01 changes
- 2: OUT10 and OUT11 change
- 3: OUT06 to OUT03 change
- 4: OUT11 to OUT07 change
- 5: All but M00 and OUT03 to OUT06 change

Be careful not to forget the "0"
![xy_grid-0006-2934360860 0](https://user-images.githubusercontent.com/122196982/214343111-e82bb20a-799b-4026-8e3c-dd36e26841e3.jpg)
### About Cache
The cache is used to store models in memory to speed up sequential merges and other operations.
Cache settings can be configured from web-ui's setting menu.

This script uses some of the web-ui and mbw-merge scripts.

# 概要
このextentionではモデルをマージした際、保存せずに画像生成用のモデルとして読み込むことができます。
これまでマージしたモデルはいったん保存して気に入らなければ削除するということが必要でしたが、このextentionを使うことでHDDやSSDの消耗を防ぐことができます。

## 使い方

### マージモード
#### Weight sum
通常のマージです。alphaが使用されます。MBWが有効になっている場合はMBWのbaseがアルファとして使われます
#### Add difference
差分マージです。MBWが有効になっている場合はMBWのbaseがアルファとして使われます
#### Triple sum
マージを3モデル同時に行います。alpha,betaが使用されます。モデル選択窓が3つあったので追加した機能ですが、有効に働かうかはわかりません。MBWでも使えます。それぞれMBWのalpha,betaを入力してください。
#### sum Twice
Weight sumを2回行います。alpha,betaが使用されます。MBWモードでも使えます。それぞれMBWのalpha,betaを入力してください。
#### Make LoRA
ふたつのモデルの差分からLoRAを生成します。生成されたLoRAはLoRAフォルダに保存されます。

### use MBW
チェックするとブロックごとのマージが有効になります。各ブロックごとの比率は下部のスライダーなどで設定してください。

### plus LoRA
LoRAをモデルに組み込みます。組み込んだ場合と通常適用した場合とで生成される画像に違いはほとんどありません。pastel mixのように複数のLoRAを組み込んだマージモデルを生成する場合や、LoRAを適応したモデルで再学習したい場合などで有効です。  
#### 使い方
LoRA名2:1,LoRA名2:0.5  
のようにLoRAの後に強度を指定します。これは画像生成時に使用する強度と同じ意味を持ちます。階層適応指定も可能で、強度の代わりに識別子を入力してください。(LoRA名:MIDD)

## 各ボタン
### merge
マージした後、生成用モデルとして読み込みます。 __左上のモデル情報とは違うモデルがロードされていることに注意してください。__ 左上のモデル選択画面でモデルを選択しなおすとリセットされます

### gen
text2imageタブの設定で画像生成を行います

### Merge and Gen
マージしたのち画像を生成します

### Save model
現在読み込まれているマージモデルを保存します(新規にマージを行います。これはロードされたモデルを保存するとfp16のモデルとして保存されるためです)

### Set from ID
マージログから設定を読み込みます。ログはマージが行われるたびに更新され、1から始まる連番のIDが付与されます。IDを生成される画像やPNG infoに記載することも可能で、write merged model ID toから設定してください。-1でSetをすると最後にマージした設定を読み出します。マージログはextention/sd-webui-supermerger/mergehistory.csvに保存されます。他アプリで開いた状態だと読み取りエラーを起こすので注意してください。Historyタブで閲覧や検索が可能です。検索は半角スペースで区切ることでand/or検索が可能です。

### Sequential XY Merge and Generation
連続マージ画像生成を行います。すべてのマージモードで有効です。
#### alpha,beta
アルファ、ベータを変更します。
#### alpha and beta
アルファ、ベータを同時に変更します。アルファ、ベータの間は半角スペースで区切り、各要素はカンマで区切ってください。数字ひとつの場合はアルファベータ共に同じ値が入力されます。  
例: 0,0.5 0.1,0.3 0.4,0.5
#### MBW
階層マージを行います。改行で区切った比率を入力してください。プリセットも使用可能ですが、改行で区切ることに注意をして下さい。Triple,Twiceの場合は２行で１セットで入力して下さい。奇数行だとエラーになります。
#### seed
シードを変更します。-1と入力すると、反対の軸方向には固定されたseedになります。
#### model_A,B,C
モデルを変更します。モデル選択窓で選択されたモデルは無視されます。
#### pinpoint blocks
MBWにおいて特定のブロックのみを変化させます。反対の軸はalphaまたはbetaを選んでください。ブロックIDを入力すると、そのブロックのみalpha(beta)が変わります。他のタイプと同様にカンマで区切ります。スペースまたはハイフンで区切ることで複数のブロックを同時に変化させることもできます。最初にNOTをつけることで変化対象が反転します。NOT IN09-OUT02とすると、IN09-OUT02以外が変化します。NOTは最初に入力しないと効果がありません。
##### 入力例
IN01,OUT10 OUT11, OUT03-OUT06,OUT07-OUT11,NOT M00 OUT03-OUT06
この場合
- 1:IN01のみ変化
- 2:OUT10およびOUT11が変化
- 3:OUT03からOUT06が変化
- 4:OUT07からOUT11が変化
- 5:M00およびOUT03からOUT06以外が変化  

となります。0の打ち忘れに注意してください。
![xy_grid-0006-2934360860 0](https://user-images.githubusercontent.com/122196982/214343111-e82bb20a-799b-4026-8e3c-dd36e26841e3.jpg)

ブロックID(大文字のみ有効)
BASE,IN00,IN01,IN02,IN03,IN04,IN05,IN06,IN07,IN08,IN09,IN10,IN11,M00,OUT00,OUT01,OUT02,OUT03,OUT04,OUT05,OUT06,OUT07,OUT08,OUT09,OUT10,OUT11

### XYプロットの予約
Reserve XY plotボタンはすぐさまプロットを実行せず、ボタンを押したときの設定のXYプロットの実行を予約します。予約したXYプロットは通常のXYプロットが終了した後か、ReservationタブのStart XY plotボタンを押すと実行が開始されます。予約はXYプロット実行時・未実行時いつでも可能です。予約一覧は自動更新されないのでリロードボタンを使用してください。エラー発生時はそのプロットを破棄して次の予約を実行します。すべての予約が終了するまで画像は表示されませんが、Finishedになったものについてはグリッドの生成は終わっているので、Image Browser等で見ることが可能です。

### キャッシュについて
モデルをメモリ上に保存することにより連続マージなどを高速化することができます。
キャッシュの設定はweb-uiのsettingから行ってください。

### unloadボタン
現在ロードされているモデルを消去します。これはkohya-ssのGUIを使用するときなどGPUメモリを開放するときに使用します。消去すると画像の生成はできません。生成する場合にはモデルを選び直して下さい。

## LoRA
LoRA関連の機能です。基本的にはkohya-ssのスクリプトと同じですが、階層マージに対応します。
### merge to checkpoint
モデルにLoRAをマージします。複数のLoRAを同時にマージできます。  
LoRA名1:マージ比率1:階層,LoRA名2:階層,マージ比率2,LoRA名3:マージ比率3･･･  
と入力します。LoRA単独でも使用可能です。「:階層」の部分は無くても問題ありません。比率はマイナスを含めどんな値でも入力できます。合計が１にならないといけないという制約もありません(もちろん大きく1を越えると破綻します)。

### Make LoRA
ふたつのモデルの差分からLoRAを生成します。
demensionを指定すると指定されたdimensionで作製されます。無指定の場合は128で作製します。

### merge LoRAs
ひとつまたはふくすうのLoRA同士をマージします。kohya-ss氏の最新のスクリプトを使用しているので、dimensionの異なるLoRA同氏もマージ可能ですが、dimensionの変換の際はLoRAの再計算を行うため、生成される画像が大きく異なる可能性があることに注意してください。  

calculate dimentionボタンで各LoRAの次元を計算して表示・ソート機能が有効化します。計算にはわりと時間がかかって、50程度のLoRAでも数十秒かかります。新しくマージされたLoRAはリストに表示されないのでリロードボタンを押してください。次元の再計算は追加されたLoRAだけを計算します。

### 通常マージとsame to Strengthの違い
same to Strengthオプションを使用しない場合は、kohya-ss氏の作製したスクリプトのマージと同じ結果になります。この場合、下図のようにWeb-ui上でLoRAを適用した場合と異なる結果になります。これはLoRAをU-netに組み込む際の数式が関係しています。kohya-ss氏のスクリプトでは比率をそのまま掛けていますが、適用時の数式では比率が２乗されてしまうため、比率を1以外の数値に設定すると、あるいはマイナスに設定するとStrength（適用時の強度）と異なる結果となります。same to Strengthオプションを使用すると、マージ時には比率の平方根を駆けることで、適用時にはStrengthと比率が同じ意味を持つように計算しています。また、マイナスが効果が出るようにも計算しています。追加学習をしない場合などはsame to Strengthオプションを使用しても問題ないと思いますが、マージしたLoRAに対して追加学習をする場合はだれも使用しない方がいいかもしれません。  
下図は通常適用/same to Strengthオプション/通常マージの各場合の生成画像です。figma化とukiyoE LoRAのマージを使用しています。通常マージの場合はマイナス方向でも２乗されてプラスになっていることが分かります。
![xyz_grid-0014-1534704891](https://user-images.githubusercontent.com/122196982/218322034-b7171298-5159-4619-be1d-ac684da92ed9.jpg)

階層別マージについては下記を参照してください

https://github.com/bbc-mc/sdweb-merge-block-weighted-gui

このスクリプトではweb-ui、mbw-merge、kohya-ssのスクリプトを一部使用しています
