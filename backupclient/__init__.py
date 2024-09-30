import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # register blueprints
    from backupclient.File import bp as file_bp
    app.register_blueprint(file_bp)

    # check for config data via pytest call or direct call.
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # A simple endpoint to check if the application booted successfully
    @app.route('/ping')
    def test_page():
        info = {
            'message': 'pong',
            'version': 'v0.1'
        }
        return info

    return app