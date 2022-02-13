import logging

from app.setup import app
import uvicorn

if __name__ == "__main__":
    # app.run()
    uvicorn.run(app, host="0.0.0.0", port=8000, lifespan="off")
