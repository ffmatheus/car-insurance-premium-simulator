from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session

from src.application.dtos.car_dto import PremiumRequestDTO
from src.application.dtos.premium_dto import PremiumResponseDTO
from src.application.services.premium_service import PremiumService
from src.domain.services.premium_calculator import PremiumCalculator
from src.infrastructure.auth.auth import get_current_api_key
from src.infrastructure.database.config import get_db
from src.infrastructure.database.models import PremiumCalculation
from src.infrastructure.database.repository import PremiumRepository


router = APIRouter(
    prefix="/premium",
    tags=["INSURANCE PREMIUM"],
    responses={404: {"description": "Not found"}},
)


def get_premium_service(db: Session = Depends(get_db)) -> PremiumService:
    premium_calculator = PremiumCalculator()
    premium_repository = PremiumRepository(db_session=db)
    return PremiumService(
        premium_calculator=premium_calculator, premium_repository=premium_repository
    )


@router.post("/calculate", response_model=PremiumResponseDTO)
async def calculate_premium(
    request: PremiumRequestDTO,
    premium_service: PremiumService = Depends(get_premium_service),
    api_key: str = Security(get_current_api_key),
) -> PremiumResponseDTO:
    try:
        return premium_service.calculate_premium(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history", response_model=List[Dict[str, Any]])
async def get_premium_history(
    skip: int = Query(0, ge=0, description="Skip N records"),
    limit: int = Query(100, ge=1, le=1000, description="Limit to N records"),
    car_make: Optional[str] = Query(None, description="Filter by car make"),
    car_model: Optional[str] = Query(None, description="Filter by car model"),
    db: Session = Depends(get_db),
    api_key: str = Security(get_current_api_key),
) -> List[Dict[str, Any]]:
    repository = PremiumRepository(db_session=db)

    filters = {}
    if car_make:
        filters["car_make"] = car_make
    if car_model:
        filters["car_model"] = car_model

    calculations = repository.get_calculations(skip=skip, limit=limit, filters=filters)

    result = []
    for calc in calculations:
        result.append(
            {
                "id": calc.id,
                "created_at": calc.created_at.isoformat(),
                "car": {
                    "make": calc.car_make,
                    "model": calc.car_model,
                    "year": calc.car_year,
                    "value": calc.car_value,
                },
                "deductible_percentage": calc.deductible_percentage,
                "broker_fee": calc.broker_fee,
                "applied_rate": calc.applied_rate,
                "policy_limit": calc.policy_limit,
                "calculated_premium": calc.calculated_premium,
            }
        )

    return result


@router.get("/history/{calculation_id}", response_model=Dict[str, Any])
async def get_premium_calculation_details(
    calculation_id: str = Path(..., description="Premium calculation ID"),
    db: Session = Depends(get_db),
    api_key: str = Security(get_current_api_key),
) -> Dict[str, Any]:
    repository = PremiumRepository(db_session=db)
    calculation = repository.get_calculation_by_id(calculation_id)

    if not calculation:
        raise HTTPException(status_code=404, detail="Calculation not found")

    return {
        "id": calculation.id,
        "created_at": calculation.created_at.isoformat(),
        "car": {
            "make": calculation.car_make,
            "model": calculation.car_model,
            "year": calculation.car_year,
            "value": calculation.car_value,
            "location": (
                {
                    "city": calculation.city,
                    "state": calculation.state,
                    "postal_code": calculation.postal_code,
                }
                if calculation.has_location
                else None
            ),
        },
        "calculation_parameters": {
            "deductible_percentage": calculation.deductible_percentage,
            "broker_fee": calculation.broker_fee,
        },
        "calculation_results": {
            "applied_rate": calculation.applied_rate,
            "base_premium": calculation.base_premium,
            "deductible_value": calculation.deductible_value,
            "policy_limit": calculation.policy_limit,
            "calculated_premium": calculation.calculated_premium,
        },
        "request_data": calculation.request_data,
        "response_data": calculation.response_data,
    }
