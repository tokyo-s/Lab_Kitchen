from fastapi import FastAPI
import uvicorn
import threading
import logging
import requests

from .Kitchen import Kitchen

app = FastAPI()
logger = logging.getLogger(__name__)

DINNING_HALL_URL = "http://dinning-hall-container:8001"


@app.post("/order")
def read_root():
    logger.warning('Order received by Kitchen')
    logger.warning('Sending foot to dining hall')
    r = requests.post(f'{DINNING_HALL_URL}/distribution')
    logging.info(f"Response status code: " + str(r.status_code))
    return {"Hello": "World"}


if __name__ == '__main__':
    threading.Thread(
        target=lambda: {
            uvicorn.run(app, host='0.0.0.0', port=8000)
        }
    ).start()

    kitchen = Kitchen()
    kitchen.run_test()
