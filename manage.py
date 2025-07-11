#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SpiderAI.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入Django。你确定它已经安装了吗？"
            "在PYTHONPATH环境变量中可用？是吗？"
            "忘记激活虚拟环境?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
