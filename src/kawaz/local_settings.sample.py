###############################################################################
#
#   本番用設定サンプル
#
###############################################################################

# Productionモードで実行する
DEBUG = False
TEMPLATE_DEBUG = False


# パターン青（深刻なエラー等）が発生した場合にメール通知を受けるための
# メールアドレスを記載
ADMINS = (
    ('管理者', 'admin@kawaz.org'),
)


# 高速化のためのキャッシュメカニズムを指定
# Ref: http://docs.djangoproject.jp/en/latest/topics/cache.html
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


# 本番用データーベースの設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}


# メール用の設定を記載
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# 管理者用のメールアドレス
# 新規会員登録がされたとき、このメールアドレス宛てに通知が届きます
REGISTRATION_NOTIFICATION_RECIPIENTS = (

)

# Sessionの暗号化などに使用されるキーを変更。
# セキュリティリスクを避けるためにこの文字列は公開してはいけない
# Ref: https://docs.djangoproject.com/en/1.7/ref/settings/#secret-key
SECRET_KEY = 'ここに十分に長いランダムな文字列'


# 本番用カレンダーID
GCAL_CALENDAR_ID = (
    ""
)

LOCAL_SETTINGS_LOADED = True
