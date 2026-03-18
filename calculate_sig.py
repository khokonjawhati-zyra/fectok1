import hmac
import hashlib

sov_id = "SOV_68007"
secret = "SOVEREIGN_QUANTUM_CORE_V15"

# Case-sensitivity normalization as per ConnectionManager.get_user_balance
u_id = sov_id.upper()

usd = 50000.14
bdt = 33307.09
coins = 0

msg = f"{u_id}:{float(usd)}:{float(bdt)}:{int(coins)}"
sig = hmac.new(secret.encode(), msg.encode(), hashlib.sha256).hexdigest()

print(f"ID: {u_id}")
print(f"USD: {usd}")
print(f"BDT: {bdt}")
print(f"COINS: {coins}")
print(f"MSG: {msg}")
print(f"SIG: {sig}")
