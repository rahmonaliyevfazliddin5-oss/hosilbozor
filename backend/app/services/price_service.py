import csv
import io
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.crop import Crop
from app.models.region import Region
from app.models.market_price import MarketPrice
from app.schemas.market_price import (
    MarketPriceCreate,
    PriceHistoryPoint,
    PriceHistoryResponse,
    CSVImportResult
)
from app.repositories.market_price_repo import market_price_repo


class PriceService:
    def get_history_chart(
        self,
        db: Session,
        crop_id: str,
        region_id: Optional[str] = None,
        days: int = 30
    ) -> PriceHistoryResponse:
        crop = db.query(Crop).filter(Crop.id == crop_id).first()
        if not crop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ekin turi topilmadi"
            )

        history_records = market_price_repo.get_price_history(db, crop_id, region_id, days)
        points = [
            PriceHistoryPoint(
                recorded_date=rec.recorded_date,
                min_price=rec.min_price,
                max_price=rec.max_price,
                avg_price=rec.avg_price,
                market_name=rec.market_name
            )
            for rec in history_records
        ]

        return PriceHistoryResponse(
            crop_id=crop_id,
            region_id=region_id,
            crop_name=crop.name_uz,
            history=points
        )

    def import_prices_from_csv(self, db: Session, file_content: bytes) -> CSVImportResult:
        """
        Parses CSV with header:
        crop_slug,region_code,market_name,min_price,max_price,avg_price,recorded_date
        """
        text = file_content.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))

        imported_count = 0
        skipped_count = 0
        errors = []

        # Cache lookups
        crops_by_slug: Dict[str, str] = {c.slug: c.id for c in db.query(Crop).all()}
        regions_by_code: Dict[str, str] = {r.code: r.id for r in db.query(Region).all()}

        row_idx = 1
        for row in reader:
            row_idx += 1
            try:
                crop_slug = row.get("crop_slug", "").strip()
                region_code = row.get("region_code", "").strip()
                market_name = row.get("market_name", "").strip()
                min_price_str = row.get("min_price", "").strip()
                max_price_str = row.get("max_price", "").strip()
                avg_price_str = row.get("avg_price", "").strip()
                date_str = row.get("recorded_date", "").strip()

                if not (crop_slug and region_code and market_name and min_price_str and avg_price_str and date_str):
                    skipped_count += 1
                    errors.append(f"Qator {row_idx}: Yetishmayotgan ustunlar mavjud.")
                    continue

                crop_id = crops_by_slug.get(crop_slug)
                if not crop_id:
                    # Try by slug lowercase
                    crop = db.query(Crop).filter(Crop.slug == crop_slug.lower()).first()
                    if crop:
                        crop_id = crop.id
                        crops_by_slug[crop_slug] = crop_id
                    else:
                        skipped_count += 1
                        errors.append(f"Qator {row_idx}: Ekin '{crop_slug}' topilmadi.")
                        continue

                region_id = regions_by_code.get(region_code)
                if not region_id:
                    region = db.query(Region).filter(Region.code == region_code.lower()).first()
                    if region:
                        region_id = region.id
                        regions_by_code[region_code] = region_id
                    else:
                        skipped_count += 1
                        errors.append(f"Qator {row_idx}: Viloyat '{region_code}' topilmadi.")
                        continue

                recorded_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                create_payload = MarketPriceCreate(
                    crop_id=crop_id,
                    region_id=region_id,
                    market_name=market_name,
                    min_price=Decimal(min_price_str),
                    max_price=Decimal(max_price_str or avg_price_str),
                    avg_price=Decimal(avg_price_str),
                    recorded_date=recorded_date
                )
                market_price_repo.record_price(db, create_payload)
                imported_count += 1

            except Exception as e:
                skipped_count += 1
                errors.append(f"Qator {row_idx}: Xatolik yuz berdi ({str(e)})")

        return CSVImportResult(
            total_rows=imported_count + skipped_count,
            imported=imported_count,
            skipped=skipped_count,
            errors=errors
        )


price_service = PriceService()
