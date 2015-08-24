__author__ = 'wangyiyang'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hellokitty',
        'USER': 'kk',
        'PASSWORD': '198610wang',
        'HOST': 'wangyiyang.cn',
        'PORT': '3306',
        # 'ATOMIC_REQUESTS': True,
        'TEST_CHARSET' :'utf8'

    }
}