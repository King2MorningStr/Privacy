
"""Local in-process API for Dimensional Cortex mobile.

This replaces the HTTP Flask API used on desktop. It wires directly into:
- Dimensional Memory (autonomic layer)
- Crystal Processing System (conscious layer)
- Dimensional Energy Regulator (physics layer)

and persists user-facing state (tier, vectors, trade) via SecureStorage.
"""

import os
import time
from typing import Dict, Any, List

from secure_storage import SecureStorage
from ui_text_system import VECTORS_AVAILABLE

# Add backend modules to path
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Import Trinity components
from dimensional_memory_constant_standalone_demo import (
    start_memory_system,
    stop_memory_system,
    EvolutionaryGovernanceEngine,
    DimensionalMemory,
)
from dimensional_processing_system_standalone_demo import (
    CrystalMemorySystem,
    GovernanceEngine,
)
from dimensional_energy_regulator import DimensionalEnergyRegulator

# -------------------------------------------------------------------------
# Secure storage bootstrap
# -------------------------------------------------------------------------

APP_SECRET = "DIMENSIONAL_CORTEX_MOBILE_V1"

def _get_device_id_path() -> str:
    base = os.path.join(BASE_DIR, "data")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "device_id.txt")

def _load_or_create_device_id() -> str:
    path = _get_device_id_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    import uuid
    device_id = uuid.uuid4().hex
    with open(path, "w", encoding="utf-8") as f:
        f.write(device_id)
    return device_id

DEVICE_ID = _load_or_create_device_id()
SECURE_DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(SECURE_DATA_DIR, exist_ok=True)
_secure_storage = SecureStorage(APP_SECRET, DEVICE_ID)
USER_STATE_PATH = os.path.join(SECURE_DATA_DIR, "user_state.enc")

# -------------------------------------------------------------------------
# Trinity initialization
# -------------------------------------------------------------------------

print("[LOCAL_API] Initializing Trinity system (mobile)...")

memory_governor, memory_system, save_thread, merge_thread = start_memory_system()

processing_governance = GovernanceEngine(data_theme="conversation")
crystal_system = CrystalMemorySystem(governance_engine=processing_governance)

energy_regulator = DimensionalEnergyRegulator(conservation_limit=50.0, decay_rate=0.1)

print("[LOCAL_API] Trinity online (mobile)")

# -------------------------------------------------------------------------
# User state (tier, vectors, trade program)
# -------------------------------------------------------------------------

DEFAULT_USER_STATE: Dict[str, Any] = {
    "tier": "free",  # 'free', 'pro', 'lifetime', 'enterprise'
    "vectors_owned": [],
    "trade_active": False,
    "trade_credits": {
        "this_month": 0.0,
        "total_lifetime": 0.0,
        "conversations_shared": 0,
        "last_payout": None,
    },
}

def _load_user_state() -> Dict[str, Any]:
    state = _secure_storage.load_json_encrypted(USER_STATE_PATH, default=None)
    if not state:
        state = DEFAULT_USER_STATE.copy()
    for k, v in DEFAULT_USER_STATE.items():
        if k not in state:
            state[k] = v
    return state

def _save_user_state(state: Dict[str, Any]) -> None:
    _secure_storage.save_json_encrypted(USER_STATE_PATH, state)

_USER_STATE = _load_user_state()

# -------------------------------------------------------------------------
# Public API functions
# -------------------------------------------------------------------------

def get_user_tier() -> Dict[str, Any]:
    """Return current user tier and rough memory usage/limit."""
    tier = _USER_STATE.get("tier", "free")
    limits = {
        "free": 10,
        "pro": 50,
        "lifetime": 50,
        "enterprise": 200,
    }
    memory_limit_gb = limits.get(tier, 10)

    # rough heuristic based on number of nodes
    try:
        current_nodes = len(memory_system.nodes)
        current_usage_gb = current_nodes * 0.001
    except Exception:
        current_usage_gb = 0.0

    return {
        "tier": tier,
        "memory_limit_gb": memory_limit_gb,
        "current_usage_gb": current_usage_gb,
    }

def upgrade_tier(new_tier: str) -> Dict[str, Any]:
    """Upgrade user tier locally.

    In a production build, this would be gated by payment confirmation.
    Here we assume payment has already succeeded when this is called.
    """
    allowed = ["pro", "lifetime", "enterprise"]
    if new_tier not in allowed:
        return {"status": "error", "message": "Invalid tier"}

    _USER_STATE["tier"] = new_tier

    if new_tier in ("pro", "lifetime"):
        _USER_STATE["vectors_owned"] = list(VECTORS_AVAILABLE.keys())

    _save_user_state(_USER_STATE)
    return {"status": "success", "new_tier": new_tier}

def get_user_vectors() -> Dict[str, Any]:
    owned = {vid: True for vid in _USER_STATE.get("vectors_owned", [])}
    return {
        "tier": _USER_STATE.get("tier", "free"),
        "vectors": owned,
    }

def purchase_vector(vector_id: str) -> Dict[str, Any]:
    if vector_id not in VECTORS_AVAILABLE:
        return {"status": "error", "message": "Unknown vector"}

    tier = _USER_STATE.get("tier", "free")
    vector_info = VECTORS_AVAILABLE[vector_id]
    if tier in ("pro", "lifetime") and vector_info.get("tier_included") == "Pro":
        return {
            "status": "success",
            "vector_id": vector_id,
            "already_included": True,
        }

    if vector_id in _USER_STATE["vectors_owned"]:
        return {
            "status": "success",
            "vector_id": vector_id,
            "already_owned": True,
        }

    _USER_STATE["vectors_owned"].append(vector_id)
    _save_user_state(_USER_STATE)
    return {"status": "success", "vector_id": vector_id}

def get_trade_status() -> Dict[str, Any]:
    import datetime

    now = datetime.datetime.now()
    next_month = (now.month % 12) + 1
    next_year = now.year if next_month > now.month else now.year + 1
    next_payout = datetime.datetime(next_year, next_month, 1)
    days_until = (next_payout - now).days

    credits = _USER_STATE["trade_credits"]
    return {
        "active": _USER_STATE.get("trade_active", False),
        "credits_this_month": credits.get("this_month", 0.0),
        "total_credits": credits.get("total_lifetime", 0.0),
        "conversations_shared": credits.get("conversations_shared", 0),
        "days_until_payout": days_until,
    }

def toggle_trade_program(active: bool) -> Dict[str, Any]:
    _USER_STATE["trade_active"] = bool(active)
    _save_user_state(_USER_STATE)
    return {
        "status": "success",
        "active": _USER_STATE["trade_active"],
    }

def calculate_trade_credits() -> Dict[str, Any]:
    """Calculate trade credits based on current Trinity state."""
    # platforms_used inferred from node payloads
    platforms_used = len(
        set(
            node.payload.get("platform")
            for node in memory_system.nodes.values()
            if isinstance(node.payload, dict)
            and node.payload.get("platform")
        )
    )

    conversation_count = len(
        [
            n
            for n in memory_system.nodes.values()
            if isinstance(n.payload, dict)
            and "conversation_id" in n.payload
        ]
    )

    try:
        diversity = len(crystal_system.crystals) / 100.0
    except Exception:
        diversity = 0.0
    pattern_diversity = min(1.0, diversity)

    credits = (platforms_used * conversation_count * pattern_diversity) / 1000.0
    credits = round(credits, 2)

    _USER_STATE["trade_credits"]["this_month"] = credits
    _USER_STATE["trade_credits"]["total_lifetime"] = round(
        _USER_STATE["trade_credits"].get("total_lifetime", 0.0) + credits, 2
    )
    _USER_STATE["trade_credits"]["conversations_shared"] = conversation_count
    _save_user_state(_USER_STATE)

    return {
        "credits_earned": credits,
        "platforms_used": platforms_used,
        "conversations": conversation_count,
        "diversity_score": round(pattern_diversity, 2),
    }

# -------------------------------------------------------------------------
# Simple ingest/query helpers
# -------------------------------------------------------------------------

def ingest_conversation(platform: str, conversation_id: str, messages: List[Dict[str, str]]):
    """Ingest a conversation into Trinity.

    messages should be list of {role, content}.
    """
    data = {
        "platform": platform,
        "conversation_id": conversation_id,
        "messages": list(messages),
        "timestamp": time.time(),
    }

    parent_node = memory_governor.ingest_data(data)

    for i, msg in enumerate(messages):
        message_data = {
            "role": msg.get("role"),
            "content": msg.get("content"),
            "index": i,
            "conversation_id": conversation_id,
            "platform": platform,
        }
        memory_governor.ingest_data(message_data, parent_node=parent_node)

    concept_name = parent_node.payload.get("concept", conversation_id)
    crystal = crystal_system.use_crystal(concept_name, data)

    role_counts: Dict[str, int] = {}
    for msg in messages:
        role = msg.get("role", "unknown")
        role_counts[role] = role_counts.get(role, 0) + 1

    for role, count in role_counts.items():
        crystal.add_facet(
            role=f"{role}_messages",
            content=f"{count} {role} messages",
            confidence=min(1.0, count / 10.0),
        )

    energy_regulator.register_crystal(crystal)
    for facet_id in crystal.facets.keys():
        energy = min(1.0, len(messages) / 20.0)
        energy_regulator.inject_energy(facet_id, energy)
    energy_regulator.step()

    presence, top_facets = energy_regulator.snapshot(top_n=5)
    return {
        "concept": concept_name,
        "crystal_level": crystal.level.name,
        "total_facets": len(crystal.facets),
        "usage_count": crystal.usage_count,
        "energy_presence": round(presence, 3),
        "top_energized_facets": [
            {"id": fid, "energy": e, "emotion": em} for fid, e, em in top_facets
        ],
    }

def get_system_stats() -> Dict[str, Any]:
    presence, top_facets = energy_regulator.snapshot(top_n=10)
    platform_stats: Dict[str, int] = {"chatgpt": 0, "claude": 0, "perplexity": 0, "other": 0}
    for node in memory_system.nodes.values():
        platform = None
        if isinstance(node.payload, dict):
            platform = node.payload.get("platform")
        platform = platform or "other"
        if platform not in platform_stats:
            platform = "other"
        platform_stats[platform] += 1

    try:
        crystal_stats = crystal_system.get_memory_stats()
    except Exception:
        crystal_stats = {}

    return {
        "memory": {
            "total_nodes": len(memory_system.nodes),
            "total_concepts": len(memory_system.concept_index),
            "platform_breakdown": platform_stats,
        },
        "crystals": crystal_stats,
        "energy": {
            "presence_scale": round(presence, 3),
            "top_facets": [
                {"id": fid, "energy": e, "emotion": em} for fid, e, em in top_facets
            ],
        },
    }
