import uvicorn

if __name__ == "__main__":
  uvicorn.run("app:app", host="http://127.0.0.1", port=8000, reload=True)