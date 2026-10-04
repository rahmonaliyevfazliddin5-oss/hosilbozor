from aiogram.fsm.state import State, StatesGroup


class FarmerListingFSM(StatesGroup):
    waiting_for_crop = State()
    waiting_for_quantity = State()
    waiting_for_price = State()
    waiting_for_description = State()
    confirm_listing = State()


class DriverBiddingFSM(StatesGroup):
    waiting_for_job_selection = State()
    waiting_for_bid_amount = State()
    waiting_for_hours = State()


class DeliveryVerificationFSM(StatesGroup):
    waiting_for_order_id = State()
    waiting_for_pickup_code = State()
    waiting_for_delivery_code = State()
    waiting_for_photo_proof = State()
