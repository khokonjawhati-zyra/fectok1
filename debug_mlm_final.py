import json
import asyncio
import websockets

async def test_mlm():
    uri = "ws://localhost:5000/ws/admin"
    user_uri = "ws://localhost:5000/ws/user"
    log_file = "debug_mlm_results_final.log"
    
    with open(log_file, "w") as f:
        f.write("Starting Final MLM Test\n")
        try:
            async with websockets.connect(user_uri) as user_ws:
                # 1. Claim session (Auto-enrolls SOV_USER_ABC)
                mesh_id = "SOV_USER_ABC"
                ref_id = "SOV_REF_XYZ"
                await user_ws.send(json.dumps({"action": "CLAIM_SESSION", "mesh_id": mesh_id}))
                
                # 2. Activate Referral (God-Mode should enroll SOV_REF_XYZ)
                await user_ws.send(json.dumps({"action": "MLM_REFERRAL_ACTIVATE", "referrer_id": ref_id}))
                
                # 3. Submit Withdrawal
                tx_id = f"TXN_{mesh_id}_FINAL"
                await user_ws.send(json.dumps({
                    "action": "A_113_TRANSACTION_SUBMIT",
                    "tx_id": tx_id,
                    "type": "WITHDRAW",
                    "vault": "WITHDRAW",
                    "amount": 100.0,
                    "currency": "USD",
                    "mesh_id": mesh_id,
                    "details": f"REQUEST: 100.0 USD via DEBUG (ID: {tx_id}) (USER: {mesh_id})"
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
                        "details": f"REQUEST: 100.0 USD via DEBUG (ID: {tx_id}) (USER: {mesh_id})"
                    }))
                    
                    f.write("Listening for MLM results...\n")
                    for _ in range(30):
                        try:
                            msg = await asyncio.wait_for(user_ws.recv(), timeout=0.5)
                            if "MLM_REWARD_CREDITED" in msg:
                                f.write(f"Referrer Reward Sync: {msg}\n")
                            if "A_113_WALLET_SYNC" in msg:
                                f.write(f"Wallet Sync: {msg}\n")
                        except:
                            pass
        except Exception as e:
            f.write(f"Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_mlm())
