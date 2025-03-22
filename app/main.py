import sys
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from api.api_v1.api import router

root = logging.getLogger("root")
root.setLevel(logging.INFO)
import settings

app = FastAPI(
    title="Add Metrics",
    description="Add Metrics"
)
app.logger = root


app.include_router(router)

@app.get("/ping", include_in_schema=False)
async def ping_server():
    return {"result": "OK"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=settings.WEB_PORT, use_colors=True,
                    log_level=logging.DEBUG, reload=True)
    except Exception as err:
        traceback.print_exc()
        print(f"failed to start server: {err}")
        sys.exit(1)
