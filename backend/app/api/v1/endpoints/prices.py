from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, UploadFile, File, status, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, require_role
from app.models.user import User, UserRole
from app.schemas.market_price import (
    MarketPriceCreate,
    MarketPriceRead,
    PriceHistoryResponse,
    PriceAlertCreate,
    PriceAlertRead,
    CSVImportResult
)
from app.repositories.market_price_repo import market_price_repo
from app.services.price_service import price_service

router = APIRouter()


@router.get("/daily", response_model=List[MarketPriceRead])
def get_daily_prices(
    region_id: Optional[str] = Query(None),
    crop_id: Optional[str] = Query(None),
    target_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    """Retrieves current wholesale prices grouped by crop and regional market."""
    return market_price_repo.get_latest_daily_prices(
        db,
        region_id=region_id,
        crop_id=crop_id,
        target_date=target_date
    )


@router.get("/history", response_model=PriceHistoryResponse)
def get_price_history_chart(
    crop_id: str = Query(...),
    region_id: Optional[str] = Query(None),
    days: int = Query(30, ge=7, le=365),
    db: Session = Depends(get_db)
):
    """Returns price trend data points for historical charts (past 7 to 365 days)."""
    return price_service.get_history_chart(db, crop_id=crop_id, region_id=region_id, days=days)


@router.post("", response_model=MarketPriceRead, status_code=status.HTTP_201_CREATED)
def record_market_price(
    payload: MarketPriceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """Manually records or updates market price entry (Admin only)."""
    return market_price_repo.record_price(db, payload)


@router.post("/import-csv", response_model=CSVImportResult, status_code=status.HTTP_200_OK)
async def import_market_prices_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    """Bulk imports daily market price indices from a CSV file (Admin only)."""
    content = await file.read()
    return price_service.import_prices_from_csv(db, content)


@router.post("/alerts", response_model=PriceAlertRead, status_code=status.HTTP_201_CREATED)
def subscribe_to_price_alert(
    payload: PriceAlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Subscribes authenticated user to price threshold alerts."""
    return market_price_repo.create_price_alert(db, user_id=current_user.id, payload=payload)


@router.get("/alerts/my", response_model=List[PriceAlertRead])
def list_my_price_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lists current user's active price alert subscriptions."""
    return market_price_repo.list_user_alerts(db, user_id=current_user.id)


@router.delete("/alerts/{id}", status_code=status.HTTP_200_OK)
def remove_price_alert(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Removes price subscription."""
    success = market_price_repo.delete_price_alert(db, user_id=current_user.id, alert_id=id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Obuna topilmadi")
    return {"success": True, "message": "Narx obunasi bekor qilindi"}
