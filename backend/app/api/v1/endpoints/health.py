from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.config import settings
from app.core.database import get_db

router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check API status and database connectivity",
)
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "connected"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        db_status = f"unhealthy: {str(exc)}"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": db_status,
    }
