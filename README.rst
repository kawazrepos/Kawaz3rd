Kawaz
===============================================================
.. image:: https://secure.travis-ci.org/kawazrepos/Kawaz3rd.svg?branch=develop
    :target: http://travis-ci.org/kawazrepos/Kawaz3rd
    :alt: Build status
.. image:: https://coveralls.io/repos/kawazrepos/Kawaz3rd/badge.png?branch=develop
    :target: https://coveralls.io/r/kawazrepos/Kawaz3rd
    :alt: Coverage
.. image:: https://requires.io/github/kawazrepos/Kawaz3rd/requirements.svg?branch=develop
     :target: https://requires.io/github/kawazrepos/Kawaz3rd/requirements/?branch=develop
     :alt: Requirements Status

**All your games are belong to us.**

札幌ゲーム製作者コミュニティ Kawaz_ のポータルサイトの開発ドキュメントです。
開発・実行は Python_ 3.5 と Django_ 1.8.7 で行われています。

.. _Kawaz: http://www.kawaz.org/
.. _Python: https://www.python.org/
.. _Django: https://www.djangoproject.com/


Kawaz をローカルにインストールする
---------------------------------------------------------------
Kawaz は `GitHub <https://github.com/kawazrepos/Kawaz3rd>`_ 上で開発されているので
下記のようにローカルにチェックアウトしてください。

.. code-block:: sh

    $ git clone https://github.com/kawazrepos/Kawaz3rd

また、上記URLではコミット権限を得られないため、開発メンバーに了承を得たコミット権のある方は
下記のように git アドレスを用いてください。

.. code-block:: sh

    $ git clone git@github.com:kawazrepos/Kawaz3rd

次に開発に必要なサブモジュールとパッケージをインストールします。
この作業は依存するサブモジュールやパッケージの更新・追加などが発生した場合に毎回行う必要があります。
**過去に動いていたのに動かなくなった場合は大抵下記の作業を行うと動くようになります**

.. code-block:: sh

    $ git submodule update --init --recursive
    $ pip install -r config/requirements.txt
    $ pip install -r config/requirements-test.txt
    $ pip install -r config/requirements-docs.txt


テストを実行する
---------------------------------------------------------------

Kawaz はテスト駆動開発により開発が進められています。
変更を加えた場合は下記の手順に従って必ずテストが通ることを確認してください。


クリーンな環境でテストを実行する場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
どの環境においてもテストが成功することを保証するためにクリーンな環境でテストを実行することを強くおすすめします。
その際は tox_ を用いて下記のように行えば自動的にクリーンな環境でのテストが実行できます（事前に ``pip install tox`` で _tox を開発環境にインストールしておいてください）。

.. code-block:: sh

    $ tox -c config/tox.ini

.. _tox: https://tox.readthedocs.org/en/latest/

開発中に簡易的にテストを実行する場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
開発時は多くの変更を加えるため上記 tox_ を利用したテストは時間がかかり面倒なことが多いと思います。
その場合は下記のように現在の環境でテストを行うと比較的高速にテストを実行することができます。

.. code-block:: sh

    $ python manage.py test kawaz                   # この場合すべての kawaz テストを実行します
    $ python manage.py test kawaz.core.personas     # この場合 kawaz.core.personas のテストのみを実行します

ただし開発環境によりインストールされているパッケージ等に差異があるため **リモートにプッシュする前に tox を利用したクリーンなテストを最低一度は実行することを強くおすすめします**


開発サーバーを実行する
---------------------------------------------------------------

デザインやクライアントサイドコードの動作確認などを行う場合は開発用サーバーにて Kawaz を起動する必要があります。
このサーバーを起動するためには

1. データベースの初期化
2. 翻訳メッセージの初期化

の手順を事前に行う必要があるので、下記のようにこれらの初期化を行なってください。

.. code-block:: sh

    $ python manage.py init_database        # データベースの初期化
    $ python manage.py compilemessages      # 翻訳メッセージの初期化

なおこの初期化は対象部分（データベース・翻訳メッセージ）に変更を加えた際はその都度実行する必要があります。

これらの初期化が終わっている場合は下記のように honcho_ を利用してサーバーを起動することができます。


.. code-block:: sh

    $ honcho start -f config/Procfile.dev

上記コマンドにより http://localhost:8000/ に開発用サーバーが http://localhost:35729/ に LiveReload_ 用サーバーが実行されます。
なお LiveReload_ 拡張が入った Google Chrome を利用するとファイル更新時に自動でブラウザの更新が呼ばれるためオススメです。

.. _honcho: https://github.com/nickstenning/honcho
.. _LiveReload: https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei


本番用サーバーを実行する
--------------------------------------------------------------

**WIP**

開発用サーバーを実行する際は下記の手順を踏んでください

1.  ``src/kawaz/local_settings.py`` を作成して下記の項目に関して設定を行う

    -   管理者のメールアドレス
    -   キャッシュ関係の設定
    -   データベースの設定
    -   メール（送信用）の設定
    -   ``SECRET_KEY`` の設定
    -   Google Calendar ID の設定
    -   その他（加筆求む）

2.  データが存在していない場合は ``python manage.py init_database`` にてデータベースの初期化を行う。
    **データが存在している場合は全データのロストにつながるため実行禁止**

3.  ``python manage.py compilemessages`` にて翻訳メッセージのコンパイルを行う。
    この作業は翻訳メッセージに変更が合った場合に毎度行う必要がある

4.  ``python manage.py collectstatic`` にて静的ファイルを ``public/static`` 以下に集める。
    この作業は静的ファイルに変更が合った場合に毎度行う必要がある

5.  ``python manage.py compress`` にて CoffeeScript/JavaScript/CSS/Less の圧縮を行う。
    この作業は上記ファイルに変更が合った場合に毎度行う必要がある


ドキュメントファイルを更新する
---------------------------------------------------------------
全てのドキュメントは ``docs`` フォルダ内に reStructuredText_ で書かれ Sphinx_ によりドキュメント化が行われている。
このドキュメントには

1.  上記のような手順書
2.  ディレクトリ構成の説明や思想説明
3.  APIドキュメント

が含まれ、``develop`` ブランチにプッシュすると自動的に KawazDevelopmentDocumentation_ に公開されます。

APIドキュメント以外の更新は適当にディレクトリ分割を行なって各自追加してください。
APIドキュメントの追加を行う場合は下記コマンドにて差分を追加できるので利用して下さい。
なおAPIドキュメントファイルを直接更新することは禁止します（変更したい場合はソースコードのコメントを修正してください）。

.. code-block:: sh

    $ sphinx-apidoc -o docs/api src -f

.. _KawazDevelopmentDocumentation: http://kawaz3rd.readthedocs.io/ja/latest/

ローカルでドキュメントをコンパイルする
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ローカルでドキュメントをコンパイルする場合は下記コマンドにより ``docs/_build/html/index.html`` （ほか多数）が作成されます。

.. code-block:: sh

    $ (cd docs; make html)

また Windows の場合は

.. code-block:: sh

    $ (cd docs; make.bat html)

でコンパイルできる（はずです）

.. _Sphinx: http://docs.sphinx-users.jp/index.html
.. _reStructuredText: http://docs.sphinx-users.jp/rest.html
