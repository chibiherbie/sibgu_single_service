import asyncio
import json

from flask import request, jsonify, abort
from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "Hello. I am alive!"


def run():
    app.run(host='0.0.0.0', port=5000)


@app.route('/api/message', methods=['POST'])
def create_task():
    from manage_data import answer
    print('SERVER', request.values)
    Thread(target=answer, args=(request.values,)).start()

    return 'Ok'


def keep_alive():
    t = Thread(target=run)
    t.start()


if __name__ == '__main__':
    keep_alive()
