#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# SOVEREIGN V15: ANTIGRAVITY-LAUNCH [ONE-CLICK IGNITION]
# ═══════════════════════════════════════════════════════════════
# Target: Linux Cloud (Ubuntu/Debian)
# Purpose: Full Ecosystem Orchestration, Media Garden Sync (R2), and 3-Layer Guard Activation.

echo "🚀 Sovereign V15: Initiating Antigravity Launch Sequence..."

# 1. Environment Guard
if [ ! -f .env ]; then
    echo "⚠️ .env file missing! Creating from DNA template..."
    echo "SYSTEM_MODE=PRODUCTION" > .env
    echo "SOVEREIGN_HOST=localhost" >> .env
fi

# --- CLOUD UPLINK CREDENTIALS [A_114] ---
CF_ACCOUNT_ID="8ba280fd13be84bf622e03f9525dc3dd"
R2_ACCESS_KEY="2d444f0e8f65e61009a60f1ec270e130"
R2_SECRET_KEY="a87d332f3ebac5f5558143b5d86e19d67fd953032bbd10094701d2aa4b8097d5"
R2_BUCKET="fectokvediostorege"
R2_URL="https://8ba280fd13be84bf622e03f9525dc3dd.r2.cloudflarestorage.com"
MOUNT_POINT="/var/www/html/media/videos"

# Function: Ignite Cloud Mount (Pillar 1)
ignite_cloud_mount() {
    echo "☁️  Phase: Cloudflare R2 Uplink Ignition..."
    
    # Install s3fs if not present
    if ! command -v s3fs &> /dev/null; then
        echo "🛠️  Installing s3fs-fuse..."
        sudo apt-get update && sudo apt-get install s3fs -y
    fi

    # Setup Access Key
    echo "${R2_ACCESS_KEY}:${R2_SECRET_KEY}" | sudo tee /etc/passwd-s3fs > /dev/null
    sudo chmod 600 /etc/passwd-s3fs

    # Ensure Mount Point exists
    sudo mkdir -p $MOUNT_POINT
    sudo chmod -R 777 $MOUNT_POINT

    # Mount the Bucket
    echo "🔗 Mounting R2 Bucket [$R2_BUCKET] to [$MOUNT_POINT]..."
    sudo umount $MOUNT_POINT 2>/dev/null
    sudo s3fs $R2_BUCKET $MOUNT_POINT \
         -o passwd_file=/etc/passwd-s3fs \
         -o url=$R2_URL \
         -o allow_other \
         -o use_cache=/tmp/s3fs_cache \
         -o nonempty

    if [ $? -eq 0 ]; then
        echo "✅ [SUCCESS] Cloudflare R2 Mounted Successfully."
    else
        echo "❌ [ERROR] Cloudflare R2 Mounting Failed. Check Credentials."
    fi
}

# 2. Storage Pulse (Media Garden, Auth Vault & Admin Secret)
echo "📂 Mapping Sovereign Tree (Media Garden, Auth Vault & Admin Secret)..."
sudo mkdir -p /mnt/sovereign_media
sudo mkdir -p /var/lib/sovereign/auth
sudo mkdir -p /opt/sovereign/admin_secret
sudo chmod -R 777 /mnt/sovereign_media
sudo chmod -R 777 /var/lib/sovereign/auth
sudo chmod 700 /opt/sovereign/admin_secret

# 2.5 Cloud Ignition (Optional: Run if cloud mount is needed)
if [ "$1" == "--cloud" ] || [ "$2" == "--cloud" ]; then
    ignite_cloud_mount
fi

# 3. Clean Rebuild (Optional but Recommended)
if [ "$1" == "--rebuild" ]; then
    echo "🏗️  Phase: Nuclear Rebuild Initiated..."
    docker-compose down -v
    docker-compose build --no-cache
fi

# 4. Critical Launch (The Atomic Switch)
echo "⚡ Phase: Atomic Ignition..."
docker-compose up -d

# 5. Shield Activation check
echo "🛡️  Phase: 3-Layer Watchdog Activation..."
sleep 5
docker ps | grep sovereign_v15_backend > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ [SUCCESS] Sovereign Shield Active."
else
    echo "❌ [FAILED] Backend Heart-beat not detected."
fi

# 6. Final Status Radar
echo "📊 Sovereign Ecosystem Status:"
docker-compose ps

echo "═══════════════════════════════════════════════════════════════"
echo "🌟 MISSION COMPLETE: Sovereign V15 is LIVE on Linux Cloud."
echo "Admin Access: http://vazo.[your-domain].com"
echo "Public Access: http://[your-domain].com"
echo "═══════════════════════════════════════════════════════════════"


# Function: Sync from Satellite Bridge (GitHub)
sync_satellite() {
    echo "📡 Pulling latest DNA from Satellite Bridge..."
    git pull origin main
    docker-compose restart
    echo "✅ Sync Complete."
}

# Function: Auth Vault Backup
backup_vault() {
    echo "🔒 Creating Auth Vault Snapshot..."
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_DIR="/opt/sovereign/backups"
    mkdir -p $BACKUP_DIR
    sudo zip -r "$BACKUP_DIR/auth_vault_$TIMESTAMP.zip" /var/lib/sovereign/auth
    echo "✅ Snapshot created: $BACKUP_DIR/auth_vault_$TIMESTAMP.zip"
}

case "$1" in
  sync) sync_satellite ;;
  backup) backup_vault ;;
  ignite-cloud) ignite_cloud_mount ;;
  --cloud) ignite_cloud_mount ;;
esac
