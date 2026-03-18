import paramiko

def mount_r2():
    host = "167.71.193.34"
    user = "root"
    pw = "vazovai11"
    
    # Credentials from antigravity-launch.sh
    R2_ACCESS_KEY = "2d444f0e8f65e61009a60f1ec270e130"
    R2_SECRET_KEY = "a87d332f3ebac5f5558143b5d86e19d67fd953032bbd10094701d2aa4b8097d5"
    R2_BUCKET = "fectokvediostorege"
    R2_URL = "https://8ba280fd13be84bf622e03f9525dc3dd.r2.cloudflarestorage.com"
    MOUNT_POINT = "/var/www/html/media/videos"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=pw, timeout=15)
        print("Connected! Initiating Cloudflare R2 Mount...")
        
        cmds = [
            # 1. Install s3fs
            "apt-get update && apt-get install s3fs -y",
            # 2. Setup passwd-s3fs
            f"echo '{R2_ACCESS_KEY}:{R2_SECRET_KEY}' | tee /etc/passwd-s3fs > /dev/null",
            "chmod 600 /etc/passwd-s3fs",
            # 3. Create mount point
            f"mkdir -p {MOUNT_POINT}",
            f"chmod -R 777 {MOUNT_POINT}",
            # 4. Unmount if busy and mount again
            f"umount {MOUNT_POINT} 2>/dev/null || true",
            f"s3fs {R2_BUCKET} {MOUNT_POINT} -o passwd_file=/etc/passwd-s3fs -o url={R2_URL} -o allow_other -o nonempty",
            # 5. Verify
            f"df -h | grep s3fs"
        ]
        
        for c in cmds:
            print(f"Executing: {c}")
            stdin, stdout, stderr = ssh.exec_command(c)
            # Wait for exit status
            exit_status = stdout.channel.recv_exit_status()
            print(f"Status: {exit_status}")
            output = stdout.read().decode().strip()
            if output:
                print(f"Output: {output}")
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    mount_r2()
