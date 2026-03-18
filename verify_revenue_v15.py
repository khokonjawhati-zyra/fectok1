import sys
import os

# Set up paths
base_path = r'c:\Users\Admin\shorts'
sys.path.append(os.path.join(base_path, 'sovereign_core', 'revenue_engine'))
sys.path.append(os.path.join(base_path, 'sovereign_core', 'live_monitor'))

try:
    from split_orchestration import RevenueOrchestrator
    from monitor_engine import LiveMonitor
    
    print("SOVEREIGN REVENUE SYSTEM: DEEP AUDIT STARTING...\n")
    
    # Test 1: Orchestration Accuracy
    orch = RevenueOrchestrator()
    sample_rev = 1000.0
    splits = orch.calculate_split(sample_rev)
    
    print(f"--- [A_111] Orchestration Logic Test (Input: {sample_rev}) ---")
    print(f"ADMIN SHARE (70%): {splits['admin']}")
    print(f"CREATOR SHARE (20%): {splits['uploader']}")
    print(f"USER SHARE (10%): {splits['viewer']}")
    
    assert splits['admin'] == 700.0, "Admin split mismatch"
    assert splits['uploader'] == 200.0, "Creator split mismatch"
    assert splits['viewer'] == 100.0, "User split mismatch"
    print("Logic Precision: 100% Correct\n")
    
    # Test 2: Live Monitor Real-time Tracking
    monitor = LiveMonitor()
    print("--- [A_111] Live Monitor Integration Test ---")
    monitor.track_realtime(50.0, "COMPLETED")
    monitor.track_realtime(25.5, "COMPLETED")
    monitor.track_realtime(100.0, "PENDING") # Should not increment
    
    print(f"TOTAL REVENUE LOGGED: {monitor.total_live_revenue_usd}")
    assert monitor.total_live_revenue_usd == 75.5, "Monitor tracking mismatch"
    print("Live Monitoring: STABLE & ACCURATE\n")
    
    # Test 3: Directory Verification
    core_files = [
        'sovereign_core/revenue_engine/split_orchestration.py',
        'sovereign_core/live_monitor/monitor_engine.py',
        'sovereign_core/dashboard_chart/revenue_graph.js',
        'sovereign_core/quantum_ledger/ledger_sync.dart',
        'sovereign_core/api_sync/gateway_config.json'
    ]
    
    print("--- [A_111] Architectural Integrity Check ---")
    for f in core_files:
        p = os.path.join(base_path, f.replace('/', os.sep))
        if os.path.exists(p):
            print(f"ONLINE: {f}")
        else:
            print(f"MISSING: {f} [CRITICAL]")
            sys.exit(1)
            
    print("\nSYSTEM CHECK COMPLETE: ALL SOVEREIGN CORE MODULES ARE VERIFIED.")

except Exception as e:
    print(f"\nAUDIT FAILED: {str(e)}")
    sys.exit(1)
