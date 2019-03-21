#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'views.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


#创建表结构
# python manage.py migrate

# python manage.py runserver 0.0.0.0:8080

# python manage.py makemigrations app
# #告诉django，myapp中的表结构有更新

# python manage.py migrate app
# #执行myapp中的表结构到mysql中

# pip install mysqlclient