###############################################################################
#
#   Kawaz ポータルサイトの設定で使用する変数の定義
#   このファイルは settings.py や local_settings.py の先頭で読み込まれることが
#   想定されている
#
###############################################################################
import os
import sys

# リポジトリルートのパスを定義
REPOSITORY_ROOT = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)
# 設定ファイル格納ディレクトリルートのパス定義
CONFIG_ROOT = os.path.join(REPOSITORY_ROOT, 'config')
# node_module系のルートディレクトリを定義
NODE_MODULES_ROOT = os.path.join(REPOSITORY_ROOT, 'node_modules')

# ライブラリ公開予定のアプリを参照するためにPYTHON_PATHに追加
LIB = os.path.join(REPOSITORY_ROOT, 'src', 'lib')
sys.path.insert(0, os.path.join(LIB, 'django-activities'))
sys.path.insert(0, os.path.join(LIB, 'django-google-calendar'))
