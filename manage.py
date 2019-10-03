# _*_coding:utf-8 _*_
# # @Author　 : Ric
from application import app, manager
from flask_script import Server
import www
import sys
import traceback

# 自定义指令,使用runserver，执行Server
manager.add_command("runserver", Server(host='0.0.0.0',
                                        port=app.config['SERVER_PORT'],
                                        use_debugger=True,
                                        use_reloader=True)
                    )


def main():
    manager.run()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc()
