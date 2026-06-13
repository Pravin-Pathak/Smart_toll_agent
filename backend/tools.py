def calculate_speed_fine(posted_limit:float, actual_speed:float) -> float:
    """
    Calculates the fine amount for overspeeding violations.
    Takes the posted speed sign limit and the actual speed of the vehicle.
    """

    if actual_speed <= posted_limit:
        return 0.0
    excess_speed = actual_speed - posted_limit
    fine = excess_speed * 100.0
    return float(fine)

def mock_toll_wallet_deduction(vehicle_id:str, total_fine_amount:float) -> str:
    """Simulates a digital wallet or FASTtag transaction deduction at the toll booth scanner.
    Takes A vehicle identification number string and the total fine amount float"""

    if total_fine_amount <= 0:
        return f"Vehicle {vehicle_id} cleared. No Outstanding fine deductions needed."

    return f"SUCCESS: Deducted ₹{total_fine_amount:.2f} from FASTtag Wallet linked to Vehicle {vehicle_id}."