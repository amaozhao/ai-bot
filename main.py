import uvicorn

from bot.app import app

if __name__ == "__main__":
    uvicorn.run(app="bot.app:app", reload=True, log_config="./bot/vuicorn.yml")
