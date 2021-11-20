from os import getenv

from dotenv import load_dotenv
from uvicorn import run

load_dotenv()

if __name__ == "__main__":
    run(
        "src:app",
        reload=bool(getenv("DEBUG")),
        port=int(getenv("PORT", "5000")),
        host="0.0.0.0",
    )
