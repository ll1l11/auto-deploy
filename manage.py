# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from auto_deploy import create_app
from auto_deploy.core import db


manager = Manager(create_app)


@manager.command
def create_all():
    db.create_all()


server = Server(host='0.0.0.0', use_debugger=True)
manager.add_command('runserver', server)


if __name__ == '__main__':
    manager.run()
