# テスト用データーベースの設定
DATABASES = {
    'TEST': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_kawaz_travis',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'connect_timeout': 60,
        },
    }
}
