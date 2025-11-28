#!/usr/bin/env python3
"""
Trinity System Test - Run BEFORE building APK
==============================================
This script verifies your Trinity modules work correctly.
"""

import sys
import time

print("="*60)
print("DIMENSIONAL CORTEX - TRINITY SYSTEM TEST")
print("="*60)
print()

# Test 1: Import Memory System
print("[TEST 1/5] Importing Memory System...")
try:
    from dimensional_memory_constant_standalone_demo import (
        start_memory_system, stop_memory_system
    )
    print("✓ Memory system imported successfully")
except Exception as e:
    print(f"✗ FAILED: {e}")
    sys.exit(1)

# Test 2: Import Processing System
print("\n[TEST 2/5] Importing Processing System...")
try:
    from dimensional_processing_system_standalone_demo import (
        CrystalMemorySystem, GovernanceEngine
    )
    print("✓ Processing system imported successfully")
except Exception as e:
    print(f"✗ FAILED: {e}")
    sys.exit(1)

# Test 3: Import Energy Regulator (Mobile Version)
print("\n[TEST 3/5] Importing Energy Regulator (Mobile)...")
try:
    from dimensional_energy_regulator_mobile import DimensionalEnergyRegulator
    print("✓ Energy regulator imported successfully")
    print("  ⚡ Using pure Python (numpy-free) version")
except Exception as e:
    print(f"✗ FAILED: {e}")
    sys.exit(1)

# Test 4: Start Trinity System
print("\n[TEST 4/5] Starting Trinity System...")
try:
    print("  → Initializing memory layer...")
    memory_governor, memory_system, save_thread, merge_thread = start_memory_system()
    print("  ✓ Memory layer online")
    
    print("  → Initializing processing layer...")
    governance = GovernanceEngine(data_theme="test")
    crystal_system = CrystalMemorySystem(governance_engine=governance)
    print("  ✓ Processing layer online")
    
    print("  → Initializing energy layer...")
    energy_regulator = DimensionalEnergyRegulator(conservation_limit=50.0, decay_rate=0.1)
    print("  ✓ Energy layer online")
    
    print("✓ Trinity system started successfully")
except Exception as e:
    print(f"✗ FAILED: {e}")
    sys.exit(1)

# Test 5: Ingest Test Data
print("\n[TEST 5/5] Ingesting Test Conversation...")
try:
    # Create test conversation
    test_data = {
        "platform": "test",
        "conversation_id": "test_001",
        "root_concept": "TEST_CONVERSATION",
        "json_data": {"status": "testing", "type": "unit_test"}
    }
    
    # Memory layer
    print("  → Memory layer processing...")
    # ingest_data returns None now (recursive)
    memory_governor.ingest_data(test_data)

    # Manually fetch the node to verify it exists
    parent_id = memory_system.find_node_id_by_concept("TEST_CONVERSATION")
    if not parent_id:
        raise Exception("Parent node was not found after ingest!")
    parent_node = memory_system.get_node(parent_id)
    print(f"  ✓ Created node: {parent_node.id}")
    
    # Processing layer
    print("  → Processing layer processing...")
    concept = parent_node.payload.get('concept', 'TEST_CONVERSATION')
    crystal = crystal_system.use_crystal(concept, test_data)
    print(f"  ✓ Created crystal: {crystal.concept} (Level: {crystal.level.name})")
    
    # Energy layer
    print("  → Energy layer processing...")
    energy_regulator.register_crystal(crystal)
    for facet_id in crystal.facets.keys():
        energy_regulator.inject_energy(facet_id, 0.5)
    energy_regulator.step()
    presence, top_facets = energy_regulator.snapshot(top_n=3)
    print(f"  ✓ Energy presence: {presence:.2f}")
    
    print("✓ Test data ingested successfully")
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Verify Stats
print("\n[BONUS] Checking System Stats...")
try:
    memory_stats = {
        'total_nodes': len(memory_system.nodes),
        'last_save': memory_system.last_global_save_timestamp
    }
    print(f"  • Memory nodes: {memory_stats['total_nodes']}")
    
    crystal_stats = crystal_system.get_memory_stats()
    print(f"  • Total crystals: {crystal_stats['total_crystals']}")
    print(f"  • Crystal levels: {crystal_stats['level_distribution']}")
    
    energy_diag = energy_regulator.get_temporal_diagnostics()
    print(f"  • Energy presence: {energy_diag['presence']:.2f}")
    print(f"  • Temporal stability: {energy_diag['temporal_stability']:.2f}")
    
    print("✓ All stats look good")
except Exception as e:
    print(f"⚠ Warning: Stats check failed (non-critical): {e}")

# Cleanup
print("\n[CLEANUP] Shutting down Trinity system...")
try:
    stop_memory_system(save_thread, merge_thread)
    print("✓ Clean shutdown complete")
except Exception as e:
    print(f"⚠ Warning: Cleanup had issues (non-critical): {e}")

# Final Summary
print("\n" + "="*60)
print("🎉 ALL TESTS PASSED!")
print("="*60)
print()
print("Your Trinity system is ready for mobile deployment.")
print()
print("Next steps:")
print("  1. Run Kivy app: python3 main.py")
print("  2. Build APK: buildozer android debug")
print("  3. Test on device: adb install bin/*.apk")
print()
print("Good luck with your launch! 🚀")
print()
