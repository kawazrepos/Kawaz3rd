# テスト用データーベースの設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kawaz_travis',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'connect_timeout': 60,
            'init_command' : 'SET foreign_key_checks = 0;SET time_zone = "+00:00"',
        },
        'STORAGE_ENGINE': 'INNODB',
    },
}
