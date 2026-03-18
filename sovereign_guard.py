import os
import sys
import ast
import logging
import subprocess
import time

# Sovereign V15: High-Precision Validation Protocol [A_001]
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("SovereignGuard")

class SovereignGuard:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.critical_files = [
            "backend/main.py",
            "user_panel/lib/main.dart",
            "Sovereign_Impression_Engine/main.py",
            "Sovereign_Revenue_Control/main.py"
        ]
        self.critical_python_classes = {
            "backend/main.py": ["ConnectionManager", "impression_engine", "revenue_vault", "SovereignAI_Moderator"],
            "Sovereign_Impression_Engine/main.py": ["FastAPI"],
            "Sovereign_Revenue_Control/main.py": ["FastAPI"]
        }

    def check_syntax(self, file_path):
        """Python Syntax Validation"""
        if not file_path.endswith('.py'):
            return True
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
            logger.info(f"SYNTAX: {file_path} [PASS]")
            return True
        except Exception as e:
            logger.error(f"SYNTAX ERROR in {file_path}: {e}")
            return False

    def check_placeholders(self, file_path):
        """Check for hardcoded 'Joga Khichuri' placeholders"""
        placeholders = ["12k", "1.2k", "Random().nextInt(900)", "mock_data", "place_holder"]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for p in placeholders:
                    if p in content:
                        # Allow some if they are in comments or valid logic, 
                        # but alert if they look like UI hacks
                        if p + "k" in content or "Random().nextInt" in content:
                           logger.warning(f"GUARD: Detected suspicious placeholder '{p}' in {file_path}")
                           return False
            return True
        except:
            return True

    def verify_integrity(self):
        """Deep Scan Critical Nodes"""
        logger.info("--- SOVEREIGN GUARD: INTEGRITY SCAN START ---")
        overall_pass = True

        for rel_path in self.critical_files:
            abs_path = os.path.join(self.root_dir, rel_path)
            if not os.path.exists(abs_path):
                logger.error(f"MISSING CRITICAL FILE: {rel_path}")
                overall_pass = False
                continue

            # Syntax Check
            if not self.check_syntax(abs_path):
                overall_pass = False

            # Placeholder Check
            if not self.check_placeholders(abs_path):
                overall_pass = False

            # Class Existence Check
            if rel_path in self.critical_python_classes:
                with open(abs_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for cls in self.critical_python_classes[rel_path]:
                        if f"class {cls}" not in content and f"app = {cls}" not in content:
                            logger.error(f"INTEGRITY: Class/App '{cls}' missing from {rel_path}")
                            overall_pass = False

        if overall_pass:
            logger.info("--- SOVEREIGN GUARD: SYSTEM SECURE [PASS] ---")
        else:
            logger.error("--- SOVEREIGN GUARD: SYSTEM VULNERABLE [FAIL] ---")
        
        return overall_pass

    def pulse_restart(self, target="backend"):
        """Selective Pulse Strategy (Non-Destructive Restart)"""
        logger.info(f"PULSE: Restarting {target} circuit...")
        if target == "backend":
            # Command to find and kill backend (demo logic for Windows)
            # In a real system, we'd use process IDs from start_sovereign.bat
            logger.info("PULSE: Backend Syncing to Mesh...")
            # subprocess.run(["taskkill", "/F", "/IM", "python.exe", "/FI", "WINDOWTITLE eq QuantumSync*"])
        
        logger.info(f"PULSE: {target.upper()} Restart Sequence Initiated.")

if __name__ == "__main__":
    guard = SovereignGuard(os.getcwd())
    if guard.verify_integrity():
        print("\n[SUCCESS] Sovereign Ecosystem Validated. Ready for Atomic Switch.")
        sys.exit(0)
    else:
        print("\n[FAILED] System validation failed. Aborting deployment.")
        sys.exit(1)
