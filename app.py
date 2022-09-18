from fastapi import FastAPI, Request
import uvicorn
import threading
import logging

from Kitchen import Kitchen

app = FastAPI()
logger = logging.getLogger(__name__)

kitchen = None


@app.post("/order")
async def get_order(request: Request):
    logger.warning('Order received by Kitchen')

    order = await request.json()
    kitchen.save_order(order)

    return {"Hello": "World"}


if __name__ == '__main__':
    threading.Thread(
        target=lambda: {
            uvicorn.run(app, host='0.0.0.0', port=8000)
        }
    ).start()

    kitchen = Kitchen()
    kitchen.run_test()
