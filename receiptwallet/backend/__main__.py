import uvicorn
from receiptwallet.backend.api import app


if __name__ == "__main__":
    uvicorn.run("receiptwallet.backend.api:app", host="0.0.0.0", port=8000, reload=True)
