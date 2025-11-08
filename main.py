from fastapi import FastAPI
from routes import ecl_routes, chat_routes, auth_routes

app = FastAPI(title="ECL Analysis API", version="1.0")

app.include_router(auth_routes.router)
app.include_router(ecl_routes.router)
app.include_router(chat_routes.router)

@app.get("/")
def root():
    return {"message": "ECL Analysis API is running!"}
