class RiskManager:
    @staticmethod
    def calculate_position_size(account_balance, risk_percent, entry_price, stop_loss):
        risk_amount = account_balance * (risk_percent / 100)
        distance = abs(entry_price - stop_loss)
        if distance == 0:
            return 0
        size = risk_amount / distance
        return round(size, 4)
