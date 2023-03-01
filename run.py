from config import site_config
from src.main import main

app = main()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("run:app", **site_config)
