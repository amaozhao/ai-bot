from bot.app import app
import uvicorn


if __name__ == "__main__":
    uvicorn.run(app="bot.app:app", reload=True)
