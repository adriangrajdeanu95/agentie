from flask_script import Manager, Shell
from agentie import app, db
import models


manager = Manager(app)

def _make_context():
    return dict(app=app, db=db, models=models)

manager.add_command("shell", Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()