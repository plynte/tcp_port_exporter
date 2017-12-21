#### Django Practice - Use Python's builtin Logging

#### settings.py
```python
LOG_LEVEL = 'DEBUG' if DEBUG else 'WARNING'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'main': {
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '%(asctime)s [%(module)s %(levelname)s] %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {

    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'main',
            'filename': os.path.join(BASE_DIR, 'logs', 'output.log')
        },
        'myhandler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'main',
            'filename': os.path.join(BASE_DIR, 'logs', 'azurecloudapi.log')
        },
    },
    'loggers': {
        # loggers 类型 为"django" 这将处理所有类型的日志
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': LOG_LEVEL,
        },
        'django.request': {
            'handlers': ['console', 'default'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'default'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'mylogger': {
            'handlers': ['console', 'myhandler'],
            'level': LOG_LEVEL,
        },
    }
}
```
> - formatters
> 定义日志输出的具体格式
> - handlers
> 定义如何处理日志，比如发送到文件，console等
> - filters
> 定义一个日志记录是否发送到handler
> - loggers
> 记录日志接口，供代码使用
> 


#### How to use logging

```python
import logging

# logger = logging.getLogger(str('mylogger'))
logger = logging.getLogger(__name__)  # 用__name__通用,自动检测

def test():
	logger.debug()
	logger.info()
	logger.warning()
	logger.error()
	logger.critical()
	#...
```
