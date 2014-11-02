# Kawazでの記事の書き方について

Kawazポータルでは、Markdownという簡単に文章の整形ができる記法が使えるほか、ブログパーツを貼り付けたりなど、多才な表現が可能です。


この記事では、Kawazでの記事の書き方についてお伝えします。

## エディタの使い方とMarkdown記法

![](../../statics/img/help/editor.png)

Kawazでは、多くの場所で上記のようなエディタを利用することができます。ここに書かれた文章は**Markdown**と呼ばれる記法で解釈されます。

これを使うことで、簡単に整形を行うことができますが、正しい書き方を知らないと、大きくデザインが崩れてしまうことがあります。


また、書きかけの文章はいつでも**プレビュー**ボタンから確認することができます。

![](../../statics/img/help/preview.png)


### 改行

初めてKawazで文章を書くときに戸惑うのが改行の扱いです。Kawazポータルでは、2行以上の改行のみが改行として出力されます。

ご注意ください。

    改行したかった
    でも改行されない


    改行したい

    二行離すとちゃんと改行される！！！


<article class="inner-markdown">
<p>改行したかった
でも改行されない</p>

<p>改行したい</p>

<p>二行離すとちゃんと改行される！！！</p>

</article>


### 見出し記法


**H1**、**H2**、**H3**と書かれたボタンを押すと、見出し記法が利用できます。

#### 例


    # 音楽ファンタジー2公開しました！

    ## 音楽ファンタジー2ってなに？

    音楽ファンタジーとは、Kawazの代表作です

    ### ストーリー

    主人公のアイズがヒロイン、キズリーと旅に出ます。



<div class="inner-markdown">

<h1>音楽ファンタジー2公開しました！</h1>

<h2>音楽ファンタジー2ってなに？</h2>

<p>音楽ファンタジーとは、Kawazの代表作です</p>

<h3>ストーリー</h3>

<p>主人公のアイズがヒロイン、キズリーと旅に出ます。<p>

</div>

このように、`#`の数によって見出しを付けることができます。

### リスト記法

<span class="glyphicon glyphicon-list"></span>ボタンを押すと、リスト記法が利用できます。

文頭に`-`を付けることで箇条書きを表現できます。また、インデントすることで入れ子のリストも表現できます


#### 例

    果物の一覧

    - りんご
    - みかん
        - オレンジ
        - いよかん
        - はっさく
    - バナナ
    - キウイ


<div class="inner-markdown">
<p>果物の一覧</p>
<ul>
<li>りんご</li>
<li>みかん
<ul>
<li>オレンジ</li>
<li>いよかん</li>
<li>はっさく</li>
</ul></li>
<li>バナナ</li>
<li>キウイ</li>
</ul>
</div>


### 番号付きリスト記法


<span class="glyphicon glyphicon-list-alt"></span>ボタンを押すと、番号付きリスト記法が利用できます。

基本的にリスト記法と同じですが、項目に番号を付けられます。


#### 例


    やること一覧

    1. 企画を立てる
    2. グラフィックを描く
        1. キャラデザをする
        2. UIを作る
    3. プログラムを書く
    4. 音楽を作る
    5. 公開する
    6. 飲みに行く


<div class="inner-markdown">
<p>やること一覧</p>

<ol>
<li>企画を立てる</li>
<li>グラフィックを描く
<ol>
<li>キャラデザをする</li>
<li>UIを作る</li>
</ol></li>
<li>プログラムを書く</li>
<li>音楽を作る</li>
<li>公開する</li>
<li>飲みに行く</li>
</ol>

</div>


### ボールド記法

<span class="glyphicon glyphicon-bold"></span>ボタンを押すと、ボールド記法（太字）が利用できます。


`** **`で囲った文字が強調されます。よく使うので覚えておくと便利。


#### 例

    Kawazは2009年に**geekdrums**によって設立された。


<div class="inner-markdown">
    <p>Kawazは2009年に<strong>geekdrums</strong>によって成立された。</p>
</div>


### イタリック記法

<span class="glyphicon glyphicon-italic"></span>ボタンを押すと、イタリック記法（斜体）が利用できます。

`* *`で囲った文字が斜体になります。固有名詞などに使われる。こちらはあまり使わないかも？


#### 例

    Kawazの代表作には、*音楽ファンタジー*などがある


<div class="inner-markdown">
    <p>Kawazの代表作には、<em>音楽ファンタジー</em>などがある</p>
</div>


### 罫線

<span class="glyphicon glyphicon-minus"></span>ボタンを押すと、罫線が利用できます。

`---------`と書くと自動的に罫線が引かれます。

話題を変えたいときに便利


#### 例

    エタノールが加水分解されることでアセトアルデヒドが生成されます。そのときに生成されるCHOをアルデヒド基と呼びます。

    --------------

    そんなことよりさっきマックで女子高生が



<div class="inner-markdown">
    <p>エタノールが加水分解されることでアセトアルデヒドが生成されます。そのときに生成されるCHOをアルデヒド基と呼びます。</p>

    <hr />

    <p>そんなことよりさっきマックで女子高生が</p>

</div>

### コードブロック記法


<span class="glyphicon glyphicon-pencil"></span>ボタンを押すと、コードブロック記法が利用できます。


ソースコードを書きたいときに<span>``` ```</span>で囲んでください

#### 例


    ```
    for (;;) {
        std::cout << "無限ループってこわくね?" << std::endl;
    }
    ```


<div class="inner-markdown">
<code>
    for (;;) {
        std::cout &lt;&lt; "無限ループってこわくね?" &lt;&lt; std::endl;
    }
</code>
</div>


### 引用


<span class="glyphicon glyphicon-book"></span>ボタンを押すと、引用が利用できます。

`> `から始まった文章は引用された文章の扱いになります。引用したいときに使いましょう


#### 例


    > よく頭のおかしいライターやクリエイター気取りのバカが
    > 「誰もやらなかった事に挑戦する」とほざくが
    > 大抵それは「先人が思いついたけどあえてやらなかった」ことだ
    > 王道が何故面白いか理解できない人間に面白い話は作れないぞ！


<div class="inner-markdown">
<blockquote>
  <p>よく頭のおかしいライターやクリエイター気取りのバカが
  「誰もやらなかった事に挑戦する」とほざくが
  大抵それは「先人が思いついたけどあえてやらなかった」ことだ
  王道が何故面白いか理解できない人間に面白い話は作れないぞ！</p>
</blockquote>
</div>


### 画像挿入


<span class="glyphicon glyphicon-picture"></span>ボタンを押すと、画像挿入が利用できます。


`![]()`に、画像の説明と画像URLを書くことで、画像を貼り付けることができます。


Web上の画像に直リンクしたいときにご利用ください。

ローカルの画像をアップロードしたい場合は、後述の**ファイルをアップロードしよう**をご覧ください。

[Gyazo](https://gyazo.com/ja)などを組み合わせると、スクリーンショットなどが簡単に貼れて便利です。


#### 例

    抜きたくなる画像

    ![抜きたくなる画像](http://i.ytimg.com/vi/Ca3lvbHHzJE/maxresdefault.jpg)


<div class="inner-markdown">
    <p>抜きたくなる画像</p>

    <p><img src="http://i.ytimg.com/vi/Ca3lvbHHzJE/maxresdefault.jpg" alt="抜きたくなる画像"></p>

</div>


### リンク挿入


<span class="glyphicon glyphicon-link"></span>ボタンを押すと、リンクが利用できます。

`[]()`に、リンクテキストと、リンク先のURLを記述してください。これもよく使うので覚えておくと便利。


#### 例


    毎年数千万円が貰える大チャンス！詳しくは[こちら](http://www.kantei.go.jp/)から！！！


<div class="inner-markdown">

    <p>毎年数千万円が貰える大チャンス！詳しくは<a href="http://www.kantei.go.jp/">こちら</a>から！！！</p>

</div>


## ファイルをアップロードしよう


<span class="glyphicon glyphicon-paperclip"></span>ボタンを押すと、アップローダーが起動します。

ここからファイルをアップロードすることができます。

Kawazでは以下のファイルに対応しています。


|ファイル形式|詳細|
|----------|----------|
|画像ファイル | 画像が埋め込まれます |
|動画ファイル | 動画プレーヤーが埋め込まれます |
|音声ファイル | 音声プレーヤーが埋め込まれます。お使いのブラウザによっては上手く動作しないかもしれません |
|PDFファイル | スライドショーが埋め込まれます |
|その他ファイル | ダウンロードリンクが埋め込まれます |

![](../../statics/img/help/uploader.png)


### その他の記法

その他、他のMarkdownで使える記法を扱うことができます。あとは自分の目で確かめよう！


[Qiita - Markdown記法 チートシート - Qiita](http://qiita.com/Qiita/items/c686397e4a0f4f11683d)


## ブログパーツを貼ろう

Kawaz3rdでは、**記事中で全てのHTMLタグを利用できるようになりました**


そのため、Kawaz2ndではできなかった、ブログパーツの貼り付けなど、多才な表現ができるようになりました。


### Twitter

<blockquote class="twitter-tweet" lang="en"><p>初めて会った人から「ゲーム作ってて彼女できた人ですね」とか、久々に会った人から「それはあなたの想像上の存在に過ぎないのではないでしょうか」とか言われたし、お前らいい加減にしろ</p>&mdash; じーく@デジゲー博D-23b (@geekdrums) <a href="https://twitter.com/geekdrums/status/485405341312499714">July 5, 2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>



### SoundCloud

<iframe width="100%" height="300" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/131592350&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;visual=true"></iframe>

### SlideShare

<iframe src="//www.slideshare.net/slideshow/embed_code/35094307" width="425" height="355" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/tunacook/ss-35094307" title="ノベルゲーム動的演出の考え方" target="_blank">ノベルゲーム動的演出の考え方</a> </strong> from <strong><a href="//www.slideshare.net/tunacook" target="_blank">tuna cook</a></strong> </div>

----

各サービスの貼り付け方は、それぞれのヘルプをご覧ください

### HTML利用の注意点

Kawazポータルでは、メンバーは全てのHTMLを利用することができるようになりましたが、HTMLの書き方によっては、ポータルのデザインを破壊してしまう可能性があります。
取り扱いには十分ご注意ください。

HTMLタグの記述ミスによるデザイン崩れなどを運営メンバーが発見した場合、規約に基づき、編集、削除を行うことがあります。

また、悪意のあるコードを故意に埋め込むような行為は絶対に控えてください。


## 動画プレイヤーを展開しよう

ニコニコ動画、YouTubeのURLを貼り付けると、自動的に動画が展開されます。


<script type="text/javascript" src="http://ext.nicovideo.jp/thumb_watch/sm6163995"></script><noscript><a href="http://www.nicovideo.jp/watch/sm6163995">【ニコニコ動画】「エヴァンミフィオン 初号兎 暴走」</a></noscript>