from flask import Flask, g, session, redirect, flash
from flask_migrate import Migrate
from flask_session import Session

from Config.BASE import config
from Config.BASE.exts import db

from Config.MODELS import UserModel

from blueprint import bp

import base64

app = Flask(__name__)
app.config.from_object(config)
Session(app)
db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(bp)


def b64encode_filter(value):
    if value:
        return base64.b64encode(value).decode('utf-8')


app.jinja_env.filters['b64encode'] = b64encode_filter


@app.before_request
def my_br():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        if user:
            setattr(g, 'user', user)
            setattr(g, 'user_id', user.id)
        else:
            session.clear()
            flash('Login session expired. Please log in again.')
            return redirect('/')
    else:
        setattr(g, 'user', None)
        setattr(g, 'user_id', None)


@app.context_processor
def my_cp():
    return {'user': g.user}


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
