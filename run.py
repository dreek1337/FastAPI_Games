from src.main import main

app = main()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("run:app", port=5000)
