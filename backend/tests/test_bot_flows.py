import pytest
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.crop import Crop
from app.models.region import Region, District
from bot.bot import create_dispatcher
from bot.fsm.states import FarmerListingFSM, DriverBiddingFSM
from bot.keyboards.main_kb import (
    get_main_menu_keyboard,
    get_crop_selection_keyboard,
    get_language_selection_keyboard
)


def test_bot_dispatcher_setup():
    dp = create_dispatcher()
    assert dp is not None
    # Verify sub-routers are attached
    assert len(dp.sub_routers) >= 4


def test_keyboards_generation():
    main_kb_uz = get_main_menu_keyboard("uz_latn")
    assert len(main_kb_uz.keyboard) >= 3
    # Verify TMA WebApp button exists
    assert any(btn.web_app is not None for row in main_kb_uz.keyboard for btn in row)

    crops_sample = [
        {"id": "crop-1", "name_uz": "Pomidor", "slug": "pomidor"},
        {"id": "crop-2", "name_uz": "Bodring", "slug": "bodring"}
    ]
    crop_kb = get_crop_selection_keyboard(crops_sample)
    assert len(crop_kb.inline_keyboard) >= 2

    lang_kb = get_language_selection_keyboard()
    assert len(lang_kb.inline_keyboard) == 2


def test_farmer_listing_fsm_states_progression():
    # Verify sequence of FSM states
    states = [
        FarmerListingFSM.waiting_for_crop,
        FarmerListingFSM.waiting_for_quantity,
        FarmerListingFSM.waiting_for_price,
        FarmerListingFSM.waiting_for_description,
        FarmerListingFSM.confirm_listing
    ]
    for s in states:
        assert s.state is not None


def test_driver_bidding_fsm_states():
    states = [
        DriverBiddingFSM.waiting_for_job_selection,
        DriverBiddingFSM.waiting_for_bid_amount,
        DriverBiddingFSM.waiting_for_hours
    ]
    for s in states:
        assert s.state is not None


def test_api_client_telegram_login_integration(client: TestClient, db: Session):
    # Verify the endpoint that the bot calls for telegram authentication works
    tg_payload = {
        "id": 99887766,
        "first_name": "Hamid",
        "username": "hamid_dehqon",
        "auth_date": 1700000000,
        "hash": "tg_auth_hash",
        "role": "farmer"
    }
    resp = client.post("/api/v1/auth/telegram-login", json=tg_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
