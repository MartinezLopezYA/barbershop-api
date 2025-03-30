import asyncio
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.models import user  # Importa tu modelo de usuario
from app.utils.database_utils import create_tables_if_not_exists

app = FastAPI()

@app.get("/test-db")
async def test_database(db: AsyncSession = Depends(get_db)):
    return {"message": "Conexión a la base de datos asíncrona exitosa"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)