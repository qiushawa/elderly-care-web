from app import app
if __name__ == '__main__':
    config = app.config
    app.run(host=config["HOST"], port=config["PORT"], debug=config["DEBUG"])