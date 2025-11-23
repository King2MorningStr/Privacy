#!/usr/bin/env python3
"""
Cortex Engine - Trinity Integration (NO FLASK)
==========================================
Direct function call engine for UDAC.
"""

import sys
import os
import time
import uuid
from typing import Any, Dict

# Add project modules to path if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import backend modules directly as they are in the Python path
from backend.dimensional_memory_constant_standalone_demo import (
    start_memory_system,
    stop_memory_system,
    EvolutionaryGovernanceEngine,
    DimensionalMemory
)
from backend.dimensional_processing_system_standalone_demo import (
    CrystalMemorySystem,
    GovernanceEngine
)
from backend.dimensional_energy_regulator import DimensionalEnergyRegulator

# Use LITE engine for Android to avoid Spacy dependency
from backend.dimensional_conversation_engine_lite import DimensionalConversationEngine

# ============================================================================
# GLOBAL TRINITY SYSTEM INITIALIZATION
# ============================================================================

class TrinitySystem:
    def __init__(self):
        print("[CORTEX] Initializing Trinity System...")

        # Memory Layer (Autonomic)
        self.memory_governor, self.memory_system, self.save_thread, self.merge_thread = start_memory_system()

        # Processing Layer (Conscious)
        self.processing_governance = GovernanceEngine(data_theme="conversation")
        self.crystal_system = CrystalMemorySystem(governance_engine=self.processing_governance)

        # Energy Layer (Physics)
        self.energy_regulator = DimensionalEnergyRegulator(conservation_limit=50.0, decay_rate=0.1)

        # Initialize LawSet
        self._init_lawset()

        # Initialize Dimensional Conversation Engine
        self.dce = DimensionalConversationEngine(
            processing_system=self.crystal_system,
            energy_regulator=self.energy_regulator,
            memory_governor=self.memory_governor
        )

        print("[CORTEX] Trinity Online. Ready for direct function calls.")

    def _init_lawset(self):
        class OpenAIChatLawSet:
            """Translates AI chat responses into DataNodes"""
            def __init__(self):
                self.name = "AI_CHAT"
                self.fingerprint_keys = {"messages", "platform", "conversation_id"}

            def analyze_data(self, data: dict, parent_law=None) -> dict:
                platform = data.get('platform', 'unknown')
                conv_id = data.get('conversation_id', f"conv_{uuid.uuid4().hex[:8]}")

                # Extract topic from first user message
                messages = data.get('messages', [])
                concept_name = conv_id

                if messages:
                    first_user = next((m for m in messages if m.get('role') == 'user'), None)
                    if first_user:
                        content = first_user.get('content', '')
                        # Use first 30 chars as concept seed
                        topic_seed = content[:30].replace(' ', '_').replace('\n', '_')
                        concept_name = f"TOPIC_{topic_seed}"

                dimensions = [
                    "dim_theme:conversation",
                    f"dim_platform:{platform}",
                    f"dim_conversation:{conv_id}"
                ]

                # Check for multi-modal content
                has_code = any('```' in m.get('content', '') for m in messages)
                if has_code:
                    dimensions.append("dim_modality:code")

                payload_update = {
                    "conversation_id": conv_id,
                    "platform": platform,
                    "message_count": len(messages),
                    "messages": messages,
                    "url": data.get('url', ''),
                    "timestamp": data.get('timestamp', time.time())
                }

                # Mutation logic
                if parent_law:
                    dimensions.append(f"dim_mutator:{parent_law.name}")

                return {
                    "concept_name": concept_name,
                    "new_dimensions": dimensions,
                    "payload_update": payload_update
                }

        # Register the new LawSet
        self.memory_governor.law_sets["AI_CHAT"] = OpenAIChatLawSet()

    def handle_interaction(self, text: str) -> str:
        """
        Main entry point for UDAC text interaction.
        Delegates to the Dimensional Conversation Engine.
        """
        if not self.dce:
            return "Error: Engine not initialized."

        try:
            response = self.dce.handle_interaction(text)
            return response
        except Exception as e:
            print(f"[ERROR] Interaction failed: {e}")
            return "I am having trouble processing that."

    def process_interaction(self, data: Dict[str, Any]):
        """
        Legacy /ingest endpoint replacement for full data objects.
        """
        try:
            # === TIER CHECKING ===
            total_nodes = len(self.memory_system.nodes)
            user_tier = data.get('user_tier', 'free')

            tier_limits = {
                'free': 1000,
                'pro': 10000,
                'enterprise': float('inf'),
                'lifetime': float('inf')
            }

            if total_nodes >= tier_limits.get(user_tier, 1000):
                return {
                    "status": "limit_reached",
                    "message": f"Limit reached for {user_tier}",
                }

            platform = data.get('platform', 'unknown')
            conv_id = data.get('conversation_id')
            messages = data.get('messages', [])

            # === STEP 1: Memory Layer ===
            parent_node = self.memory_governor.ingest_data(data)

            for i, msg in enumerate(messages):
                message_data = {
                    "role": msg.get('role'),
                    "content": msg.get('content'),
                    "index": i,
                    "conversation_id": conv_id,
                    "platform": platform
                }

                self.memory_governor.ingest_data(
                    message_data,
                    parent_node=parent_node,
                    parent_law_object=self.memory_governor.law_sets["AI_CHAT"]
                )

            # === STEP 2: Processing Layer ===
            concept_name = parent_node.payload.get('concept', conv_id)
            crystal = self.crystal_system.use_crystal(concept_name, data)

            # Add facets
            role_counts = {}
            for msg in messages:
                role = msg.get('role', 'unknown')
                role_counts[role] = role_counts.get(role, 0) + 1

            for role, count in role_counts.items():
                crystal.add_facet(
                    role=f"{role}_messages",
                    content=f"{count} {role} messages",
                    confidence=min(1.0, count / 10.0)
                )

            # === STEP 3: Energy Layer ===
            self.energy_regulator.register_crystal(crystal)

            message_count = len(messages)
            for facet_id in crystal.facets.keys():
                energy = min(1.0, message_count / 20.0)
                self.energy_regulator.inject_energy(facet_id, energy)

            self.energy_regulator.step()
            presence, top_facets = self.energy_regulator.snapshot(top_n=5)

            return {
                "status": "success",
                "conversation_id": conv_id,
                "concept": concept_name,
                "crystal_level": crystal.level.name,
                "energy_presence": round(presence, 3)
            }

        except Exception as e:
            print(f"[ERROR] Ingestion failed: {e}")
            return {"status": "error", "message": str(e)}

    def shutdown(self):
        print("\n[CORTEX] Shutting down Trinity...")
        stop_memory_system(self.save_thread, self.merge_thread)
