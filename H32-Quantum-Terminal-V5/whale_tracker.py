import pandas as pd
import datetime

class WhaleMemory:
    def __init__(self):
        # Whale history ko store karne ke liye dataframe
        self.history_file = "whale_history.csv"
        try:
            self.history = pd.read_csv(self.history_file)
        except:
            self.history = pd.DataFrame(columns=['wallet', 'time', 'amount', 'type', 'balance_change'])

    def record_movement(self, wallet_id, amount, move_type):
        """
        Record karega ke whale ne kab kitna nikala ya dala.
        move_type: 'IN' (Exchange pe laya), 'OUT' (Exchange se nikala)
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Purani history check karna
        prev_moves = self.history[self.history['wallet'] == wallet_id]
        total_prev = prev_moves['amount'].sum() if not prev_moves.empty else 0
        
        # New entry
        new_entry = {
            'wallet': wallet_id,
            'time': current_time,
            'amount': amount,
            'type': move_type,
            'history_summary': f"Previously moved: ${total_prev:,.2f}"
        }
        
        # Save to CSV (Storage)
        self.history = pd.concat([self.history, pd.DataFrame([new_entry])], ignore_index=True)
        self.history.to_csv(self.history_file, index=False)
        return new_entry
