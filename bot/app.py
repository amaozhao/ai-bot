from fastapi import FastAPI


def application():
    return FastAPI(debug=True, title="bot", version="0.0.1")

app = application()


@app.get("/")
async def root():
    return {"message": "Hello World"}