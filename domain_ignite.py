import paramiko
import time

def setup_domains():
    host = "167.71.193.34"
    password = "c69bbe78dd586755897741cef3"
    user = "root"
    
    print(f"📡 Setting up Sovereign Domain Registry on {host}...")
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password, timeout=20)
        
        print("--- [SUCCESS] Connection Active ---")
        
        # 1. Set Hostname
        print("Setting Hostname to fectok.com...")
        client.exec_command("hostnamectl set-hostname fectok.com")
        
        # 2. Update /etc/hosts
        print("Mapping vazo.fectok.com to local loopback...")
        client.exec_command("echo '127.0.0.1 fectok.com vazo.fectok.com' >> /etc/hosts")
        
        # 3. Verify
        stdin, stdout, stderr = client.exec_command("hostname")
        new_host = stdout.read().decode().strip()
        print(f"Verified Hostname: {new_host}")
        
        client.close()
        print("\n--- [MISSION COMPLETE] Server is now domain-aware. ---")
    except Exception as e:
        print(f"Setup Failed: {e}")

if __name__ == "__main__":
    setup_domains()
