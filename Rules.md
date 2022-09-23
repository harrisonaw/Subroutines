# 開発する上で必要な知識

## FORTRAN77 を書く上でのルール

- 大文字小文字の区別はない
- 1 行は 7-72 列の 66 文字まで書ける
- コメントは"!"または"c"を用いる
- 一行に入りきらない場合は"\&"または数字を用いて次の行につなげることが可能
- 暗黙の型宣言の無効化が推奨される(implicit none)
- PARAMETER 文は代入文より先に書かなければならない
- キーワード引数は使えない(コンパイラによるっぽい、ABAQUS は無理)
- PRESENT 文は OPTIONAL 引数に対してのみ使用できる
- OPTIONAL 文は書かなくても良い(書かなくても引数は省略可能)
- 加算代入、減算代入はできない
- 各計算用組込関数には個別名と総称名がある
- サブルーチンに配列を渡す際は配列の先頭要素を指定しても良いし、配列そのものを直接指定しても良い
- 配列の出力には`WRITE(6,*) STRESS`のように配列名を書くだけで良い(インデックスの記述はいらない)
- 配列同士の加減乗除はインデックスを使わなくても可能、配列とスカラーも同様
- 行列に配列を代入することも可能(スライスを用いて指定する, a(1,:) = b など)
- function を宣言する際、型の宣言は引数の順に宣言する必要がある?
- function で配列を返すことができる(が、ABAQUS では上手くいかないので配列を返す場合 subroutine を使うべき)
- 一次配列、二次配列の計算用に dot_product,matmul という組込関数がある
- 変数の宣言文と初期化文は必ず分けること(コンパイルエラーになったり、意図しない値が入ったりする)
- 倍精度実数変数に単精度の値を代入すると意図しない値が入ってしまうので注意(必ず D0 というように桁をつける)
- fortran は列優先なので行列の各要素にアクセスするループを書く場合は一列ごとに処理を回した方が早くなる(キャッシュヒット率が上がる)
- プロセスを終了させるためには EXIT という subroutine を call すれば良い。これは DO 文のループを抜ける際にも利用できる
- 計算途中で NaN が発生すると、それを用いた計算の結果は全て NaN になっていく
- 計算結果が NaN かどうかを判定する isnan という組込関数がある

## ABAQUS でサブルーチンを実装する上で必要な知見

- ABAQUS とは関係のないファイルに出力することはできなそう(OPEN してそこに WRITE するのは無理っぽい)
- WRITE 文 の装置識別子は dat ファイルに出力する場合 6,msg ファイルに出力する場合 7 を用いる
- STRESS に格納されている値は xx,yy,zz,xy,xz,yz の順([参考](https://abaqus-docs.mit.edu/2017/English/SIMACAEMODRefMap/simamod-c-conventions.htm#simamod-c-conventions-t-ConventionUsedForStressAndStrainComponents-sma-topic16))
- UMAT のサブルーチンを実装して利用する場合、それが適用されるのは"ユーザー定義材料特性"が定義されているマテリアルが使用されているパートのみ
- 上記のユーザー定義材料特性は UMAT で PROPS という配列内に保存されている
- ステップをまたいで使用したい変数は STATEV という配列に格納すれば良い(配列のサイズは ABAQUS の"材料特性の編集"ウィンドウの"解依存の状態変数"から定義できる)

### UMAT で行わなければならないこと二つ

- STRESS を更新する
- DDSDDE(ヤコビ行列)を返す

  ABAQUS の陰解法で用いられるヤコビ行列を返す必要があり、これは収束できる程度に正確であれば良い。
  ちなみに DDSDDE という変数名の由来は ∂Δs/∂Δε を読み上げるときの頭文字を取ったものだと思われる。

### ABAQUS 組込サブルーチンに関して

- 座標軸に応じてテンソルの回転を行ってくれる ROTSIG というサブルーチンがある
- テンソルの主値を計算することができる SPRINC というサブルーチンが存在する。非常に便利
- 解析をストップできる XIT というサブルーチンがある

## 実装する上でのルール(2020/4)

以下重要度の高い順

- ABAQUS 由来の組込関数、組込変数、FORTRAN の組込関数、ユーザー定義の定数は全て大文字とする
- ユーザー定義の変数、関数、サブルーチンは全て lowerCamel とする
- 変数名の接頭辞
  |接頭辞|意味|
  |:--:|:--:|
  |e|弾性|
  |p|塑性|
  |eq|相当|
  |d|微分|
  |Db|double|
  |pri|主値,principal の pri|
  |yld|降伏関数に関する変数|
  |G|塑性ポテンシャル|
  |hard|硬化則に関する変数|
  |num|数量|

  eqpStrain: 相当塑性ひずみ

  numIteration: 繰り返しの数

  sPrime: s'

  sDbPrime: s"

  yldT: yld2004 で使用するテンソル T

- 接頭辞が変数名の途中に付く場合は必ず小文字
- 接頭辞が変数名の途中にあり、かつ見づらい場合は snake case で記述する(calc から始まる subroutine が多いため、これらは全て snake case)
- 配列に代入するときは、それが配列だとわかるよう、(:)を用いて明示的にする
- 大文字と小文字が入り乱れるので、変数名が重複しないように注意する