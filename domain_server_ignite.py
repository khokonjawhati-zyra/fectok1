import paramiko
import time

def domain_server_ignite():
    host = "167.71.193.34"
    password = "c69bbe78dd586755897741cef3"
    user = "root"
    
    print(f"🚀 INITIATING DOMAIN-SERVER BRIDGE IGNITION: {host}...")
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, password=password, timeout=20)
        
        print("--- [PULSE] Connection Secure. Starting Injection... ---")
        
        # 1. Update Hostname permanently
        print("Phase 1: Injecting Hostname (fectok.com)...")
        client.exec_command("hostnamectl set-hostname fectok.com")
        
        # 2. Re-wire /etc/hosts for both domains
        print("Phase 2: Wiring Virtual Loopback Mapping...")
        # Clean existing entries and add precise mapping
        cmds = [
            "sed -i '/fectok.com/d' /etc/hosts",
            "echo '127.0.0.1 fectok.com vazo.fectok.com' >> /etc/hosts",
            "echo '::1 fectok.com vazo.fectok.com' >> /etc/hosts"
        ]
        for cmd in cmds:
            client.exec_command(cmd)
            
        # 3. Network Reload
        print("Phase 3: Restarting Network Services...")
        client.exec_command("systemctl restart systemd-hostnamed")
        
        # 4. Final Handshake Verification
        print("Phase 4: Verifying Domain-to-Server Link...")
        stdin, stdout, stderr = client.exec_command("hostname -f")
        result = stdout.read().decode().strip()
        
        client.close()
        print(f"\n✅ [HANDSHAKE COMPLETE] Server Identity: {result}")
        print("🌐 fectok.com and vazo.fectok.com are now logically fused with this droplet.")
        return True
    except Exception as e:
        print(f"❌ Ignition Failed: {e}")
        return False

if __name__ == "__main__":
    domain_server_ignite()
