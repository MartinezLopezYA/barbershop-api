from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db

from app.api.controllers import user, role

app = FastAPI()

app.include_router(user.user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(role.role_router, prefix="/api/v1/roles", tags=["roles"])

@app.get("/test-db")
async def test_database(db: AsyncSession = Depends(get_db)):
    return {"message": "Conexión a la base de datos asíncrona exitosa"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)