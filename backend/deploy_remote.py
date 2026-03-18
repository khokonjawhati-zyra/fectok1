import paramiko
import os
import sys

# ═══════════════════════════════════════════════════════════════
# SOVEREIGN V15: AUTOMATIC LIVE NODE DEPLOYER [A_124 Armed]
# ═══════════════════════════════════════════════════════════════

HOST = "167.71.193.34"
USER = "lovetok"
PASS = "uE?jgthTu2!97X5k"

def deploy():
    print(f"Connecting to Sovereign Node at {HOST}...")
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, username=USER, password=PASS)
        print("SECURE_AUTH: Succeeded.")

        # 1. CREATE PROJECT DIRECTORY
        sftp = ssh.open_sftp()
        try:
            sftp.mkdir("/home/lovetok/sovereign_v15_backend")
        except:
            pass
        
        # 2. UPLOAD BACKEND CORE
        print("UPLOADING: main.py -> Remote Node")
        sftp.put("main.py", "/home/lovetok/sovereign_v15_backend/main.py")
        
        # 3. INITIALIZE STORAGE [A_113 Pulse]
        print("INITIALIZING: config & pool files...")
        
        # Ensure bridge_config.json exists locally or create dummy
        if not os.path.exists("bridge_config.json"):
            with open("bridge_config.json", "w") as f:
                f.write('{"webhook_key": "SOV_V15_GOD_MODE_777", "numbers": {"bkash": "017...", "nagad": "018...", "rocket": "019..."}}')
        
        sftp.put("bridge_config.json", "/home/lovetok/sovereign_v15_backend/bridge_config.json")
        
        # Empty pool if not exists
        if not os.path.exists("sms_payment_pool.json"):
            with open("sms_payment_pool.json", "w") as f:
                f.write('[]')
        sftp.put("sms_payment_pool.json", "/home/lovetok/sovereign_v15_backend/sms_payment_pool.json")

        # 4. INSTALL REMOTE DEPENDENCIES
        print("INSTALLING: Remote Cloud Dependencies...")
        commands = [
            "sudo apt-get update -y",
            "sudo apt-get install python3-pip -y",
            "pip3 install fastapi uvicorn pydantic requests"
        ]
        
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # Wait for execution to finish
            stdout.channel.recv_exit_status()
            print(f"EXEC: {cmd}")

        # 5. FIREWALL IGNITION [Port 5000 Open]
        print("FIREWALL: Opening Port 5000...")
        ssh.exec_command("sudo ufw allow 5000")

        # 6. START SERVER IN BACKGROUND (USING SCREEN)
        print("IGNITION: Starting Sovereign Mesh Node...")
        ssh.exec_command("sudo apt-get install screen -y")
        ssh.exec_command("screen -S sovereign_node -dm bash -c 'cd /home/lovetok/sovereign_v15_backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 5000'")
        
        print("\n" + "="*40)
        print("Sovereign Node is now LIVE at http://167.71.193.34:5000")
        print("="*40)

        sftp.close()
        ssh.close()

    except Exception as e:
        print(f"CRITICAL_DEPLOY_ERR: {e}")

if __name__ == "__main__":
    deploy()
