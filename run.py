# from app import app
from app import create_app, db

app = create_app('dev')
app.app_context().push()

if __name__ == '__main__':
    app.run(port=8000)