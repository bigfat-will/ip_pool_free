
from flask import Flask
from db.db_client import DbClient

app = Flask(__name__)


@app.route("/")
def index():
    return DbClient().get_ip_list()


def run():
    app.run(host='0.0.0.0', port=10000)


if __name__ == '__main__':
    print("api")
    app.run(host='0.0.0.0', port=10000)