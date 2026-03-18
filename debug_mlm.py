import json
import asyncio
import websockets

async def test_mlm():
    uri = "ws://localhost:5000/ws/admin"
    user_uri = "ws://localhost:5000/ws/user"
    log_file = "debug_mlm_results.log"
    
    with open(log_file, "w") as f:
        f.write("Starting MLM Test\n")
        try:
            async with websockets.connect(user_uri) as user_ws:
                # 1. Claim session
                user_id = "SOV_GHOST_1"
                referrer_id = "SOV_MASTER_1"
                await user_ws.send(json.dumps({
                    "action": "CLAIM_SESSION",
                    "mesh_id": user_id
                }))
                
                # 2. Wait for claim ack and activation
                await user_ws.send(json.dumps({
                    "action": "MLM_REFERRAL_ACTIVATE",
                    "referrer_id": referrer_id
                }))
                
                # 3. Submit Withdrawal
                tx_id = f"TXN_{user_id}_123"
                await user_ws.send(json.dumps({
                    "action": "A_113_TRANSACTION_SUBMIT",
                    "tx_id": tx_id,
                    "type": "WITHDRAW",
                    "vault": "WITHDRAW",
                    "amount": 100.0,
                    "currency": "USD",
                    "mesh_id": user_id,
                    "details": f"REQUEST: 100.0 USD (USER: {user_id})"
                }))
                
                async with websockets.connect(uri) as admin_ws:
                    # 4. Approve Withdrawal
                    await admin_ws.send(json.dumps({
                        "action": "A_113_TRANSACTION_DECISION",
                        "tx_id": tx_id,
                        "vault": "WITHDRAW",
                        "decision": "APPROVED",
                        "amount": 100.0,
                        "currency": "USD",
                        "details": f"REQUEST: 100.0 USD (USER: {user_id})"
                    }))
                    
                    # 5. Listen for results
                    f.write("Listening for responses...\n")
                    for _ in range(20):
                        try:
                            # Listen to both or just admin
                            msg = await asyncio.wait_for(admin_ws.recv(), timeout=1.0)
                            f.write(f"Admin Msg: {msg}\n")
                        except:
                            pass
                        try:
                            msg = await asyncio.wait_for(user_ws.recv(), timeout=1.0)
                            f.write(f"User Msg: {msg}\n")
                        except:
                            pass
        except Exception as e:
            f.write(f"Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_mlm())
