from flask import Flask, request
import threading
import logging

from Kitchen import Kitchen

app = Flask(__name__)
logger = logging.getLogger(__name__)

kitchen = None

@app.route('/order', methods=['POST'])
def get_order():
    logger.warning('Order received by Kitchen')
    order = request.json
    kitchen.save_order(order)

    return {}


if __name__ == '__main__':
    threading.Thread(
        target=lambda: {
            app.run(debug=True, use_reloader=False, host="0.0.0.0", port=8000)
        }
    ).start()

    kitchen = Kitchen()
    kitchen.run_test()
