#!/usr/bin/env python3
"""
Cortex Local Server - Trinity Integration
==========================================
Receives AI responses from browser extension and feeds them into the Dimensional system.
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os
import time
import uuid

# Add project modules to path
sys.path.insert(0, '/mnt/project')

from dimensional_memory_constant_standalone_demo import (
    start_memory_system,
    stop_memory_system,
    EvolutionaryGovernanceEngine,
    DimensionalMemory
)
from dimensional_processing_system_standalone_demo import (
    CrystalMemorySystem,
    GovernanceEngine
)
from dimensional_energy_regulator import DimensionalEnergyRegulator

app = Flask(__name__)
CORS(app)  # Allow requests from browser extension

# ============================================================================
# GLOBAL TRINITY SYSTEM INITIALIZATION
# ============================================================================

print("[CORTEX] Initializing Trinity System...")

# Memory Layer (Autonomic)
memory_governor, memory_system, save_thread, merge_thread = start_memory_system()

# Processing Layer (Conscious)
processing_governance = GovernanceEngine(data_theme="conversation")
crystal_system = CrystalMemorySystem(governance_engine=processing_governance)

# Energy Layer (Physics)
energy_regulator = DimensionalEnergyRegulator(conservation_limit=50.0, decay_rate=0.1)

print("[CORTEX] Trinity Online. Server ready on http://localhost:5000")

# ============================================================================
# OPENAI CHAT LAWSET (NEW)
# ============================================================================

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
memory_governor.law_sets["AI_CHAT"] = OpenAIChatLawSet()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/ingest', methods=['POST'])
def ingest():
    """
    Receives AI conversation data from browser extension.
    Feeds it through the Trinity system.
    """
    try:
        data = request.json
        
        # === TIER CHECKING ===
        total_nodes = len(memory_system.nodes)
        user_tier = data.get('user_tier', 'free')  # Extension sends this
        
        # Tier limits
        tier_limits = {
            'free': 1000,
            'pro': 10000,
            'enterprise': float('inf'),
            'lifetime': float('inf')
        }
        
        if total_nodes >= tier_limits.get(user_tier, 1000):
            return jsonify({
                "status": "limit_reached",
                "message": f"You've reached the {user_tier.upper()} tier limit of {tier_limits[user_tier]} conversations.",
                "current_count": total_nodes,
                "upgrade_url": "http://localhost:5000/upgrade"
            }), 403
        
        platform = data.get('platform', 'unknown')
        conv_id = data.get('conversation_id')
        message_count = len(data.get('messages', []))
        
        print(f"\n[INGEST] Received {message_count} messages from {platform} (conv: {conv_id})")
        print(f"[TIER] User: {user_tier} | Nodes: {total_nodes}/{tier_limits[user_tier]}")
        
        # === STEP 1: Memory Layer (Autonomic Storage) ===
        
        # === STEP 1: Memory Layer (Autonomic Storage) ===
        # Ingest into dimensional memory with generational linking
        parent_node = memory_governor.ingest_data(data)
        
        # Ingest each message as a child node
        messages = data.get('messages', [])
        for i, msg in enumerate(messages):
            message_data = {
                "role": msg.get('role'),
                "content": msg.get('content'),
                "index": i,
                "conversation_id": conv_id,
                "platform": platform
            }
            
            memory_governor.ingest_data(
                message_data,
                parent_node=parent_node,
                parent_law_object=memory_governor.law_sets["AI_CHAT"]
            )
        
        # === STEP 2: Processing Layer (Crystal Evolution) ===
        # Extract concept name
        concept_name = parent_node.payload.get('concept', conv_id)
        
        # Use crystal (triggers evolution check)
        crystal = crystal_system.use_crystal(concept_name, data)
        
        # Add facets for each message role type
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
        
        # === STEP 3: Energy Layer (Physics) ===
        # Register crystal facets with energy regulator
        energy_regulator.register_crystal(crystal)
        
        # Inject energy based on message count (more messages = more energy)
        for facet_id in crystal.facets.keys():
            energy = min(1.0, message_count / 20.0)
            energy_regulator.inject_energy(facet_id, energy)
        
        # Run physics tick
        energy_regulator.step()
        
        # Get energy snapshot
        presence, top_facets = energy_regulator.snapshot(top_n=5)
        
        # === STEP 4: Response ===
        response = {
            "status": "success",
            "conversation_id": conv_id,
            "concept": concept_name,
            "crystal_level": crystal.level.name,
            "total_facets": len(crystal.facets),
            "usage_count": crystal.usage_count,
            "energy_presence": round(presence, 3),
            "top_energized_facets": [
                {"id": fid, "energy": e, "emotion": em} 
                for fid, e, em in top_facets
            ],
            "memory_stats": memory_system.get_memory_stats() if hasattr(memory_system, 'get_memory_stats') else {},
            "nodes_created": len(messages) + 1
        }
        
        print(f"[TRINITY] Processed: {concept_name} | Level: {crystal.level.name} | Facets: {len(crystal.facets)} | Energy: {presence:.2f}")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"[ERROR] Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/query', methods=['POST'])
def query():
    """
    Retrieves context for a given topic/conversation.
    Returns Crystal state + top energy facets + relevant memory nodes.
    """
    try:
        data = request.json
        query_text = data.get('query', '')
        conversation_id = data.get('conversation_id')
        
        print(f"\n[QUERY] Looking for: {query_text or conversation_id}")
        
        results = {
            "crystals": [],
            "memory_nodes": [],
            "energy_state": {}
        }
        
        # Search crystals
        for crystal in crystal_system.crystals.values():
            if conversation_id and conversation_id in crystal.concept:
                results["crystals"].append({
                    "concept": crystal.concept,
                    "level": crystal.level.name,
                    "facet_count": len(crystal.facets),
                    "usage_count": crystal.usage_count,
                    "last_used": crystal.last_used
                })
            elif query_text.lower() in crystal.concept.lower():
                results["crystals"].append({
                    "concept": crystal.concept,
                    "level": crystal.level.name,
                    "facet_count": len(crystal.facets),
                    "usage_count": crystal.usage_count
                })
        
        # Search memory nodes
        for node_id, node in memory_system.nodes.items():
            concept = node.payload.get('concept', '')
            if conversation_id and conversation_id in concept:
                results["memory_nodes"].append({
                    "id": node_id,
                    "concept": concept,
                    "payload": node.payload,
                    "links": node.dimension_links[:5]  # Top 5 links only
                })
            elif query_text and query_text.lower() in concept.lower():
                results["memory_nodes"].append({
                    "id": node_id,
                    "concept": concept,
                    "payload": node.payload
                })
        
        # Energy diagnostics
        results["energy_state"] = energy_regulator.get_temporal_diagnostics()
        
        print(f"[QUERY] Found {len(results['crystals'])} crystals, {len(results['memory_nodes'])} nodes")
        
        return jsonify(results)
        
    except Exception as e:
        print(f"[ERROR] Query failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Returns system-wide statistics with platform breakdown"""
    presence, top_facets = energy_regulator.snapshot(top_n=10)
    
    # Calculate platform-specific stats
    platform_stats = {"chatgpt": 0, "claude": 0, "perplexity": 0, "other": 0}
    for node in memory_system.nodes.values():
        platform = node.payload.get('platform', 'other')
        if platform in platform_stats:
            platform_stats[platform] += 1
        else:
            platform_stats['other'] += 1
    
    return jsonify({
        "memory": {
            "total_nodes": len(memory_system.nodes),
            "total_concepts": len(memory_system.concept_index),
            "platform_breakdown": platform_stats
        },
        "crystals": crystal_system.get_memory_stats(),
        "energy": {
            "presence_scale": round(presence, 3),
            "temporal_diagnostics": energy_regulator.get_temporal_diagnostics(),
            "top_facets": [
                {"id": fid, "energy": e, "emotion": em}
                for fid, e, em in top_facets
            ]
        },
        "governance": {
            "total_laws_applied": processing_governance.total_laws_applied,
            "assessment_count": len(memory_governor.assessment_log)
        }
    })

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Serves the dashboard UI"""
    return send_file('dashboard.html')

@app.route('/upgrade', methods=['GET'])
def upgrade():
    """Serves the upgrade/pricing page"""
    return send_file('upgrade.html')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "trinity": {
            "memory": "online",
            "processing": "online",
            "energy": "online"
        }
    })

# ============================================================================
# USER TIER & SUBSCRIPTION ENDPOINTS
# ============================================================================

# In-memory user data (replace with database in production)
USER_DATA = {
    "tier": "free",  # free, pro, lifetime
    "vectors_owned": [],  # list of vector IDs
    "trade_active": False,
    "trade_credits": {
        "this_month": 0.0,
        "total_lifetime": 0.0,
        "conversations_shared": 0,
        "last_payout": None
    }
}

@app.route('/user/tier', methods=['GET'])
def get_user_tier():
    """Returns current user tier"""
    return jsonify({
        "tier": USER_DATA["tier"],
        "memory_limit": {
            "free": 10,
            "pro": 50,
            "lifetime": 50
        }[USER_DATA["tier"]],
        "current_usage_gb": len(memory_system.nodes) * 0.001  # Rough estimate
    })

@app.route('/user/tier/upgrade', methods=['POST'])
def upgrade_tier():
    """Upgrade user tier (after payment processing)"""
    data = request.json
    new_tier = data.get('tier')  # 'pro' or 'lifetime'
    payment_token = data.get('payment_token')  # From Stripe
    
    # TODO: Verify payment with Stripe
    # For now, just update tier
    if new_tier in ['pro', 'lifetime']:
        USER_DATA["tier"] = new_tier
        
        # Pro/Lifetime get all Pro vectors automatically
        USER_DATA["vectors_owned"] = [
            "predictive_foresight",
            "emotional_gradient",
            "introspection",
            "relational_dynamics"
        ]
        
        return jsonify({
            "status": "success",
            "new_tier": new_tier,
            "message": "Upgrade successful!"
        })
    
    return jsonify({"status": "error", "message": "Invalid tier"}), 400

@app.route('/user/vectors', methods=['GET'])
def get_user_vectors():
    """Returns user's owned vectors"""
    return jsonify({
        "vectors": {vid: True for vid in USER_DATA["vectors_owned"]},
        "tier": USER_DATA["tier"]
    })

@app.route('/user/vectors/purchase', methods=['POST'])
def purchase_vector():
    """Purchase individual vector"""
    data = request.json
    vector_id = data.get('vector_id')
    payment_token = data.get('payment_token')
    
    # TODO: Verify payment
    if vector_id and vector_id not in USER_DATA["vectors_owned"]:
        USER_DATA["vectors_owned"].append(vector_id)
        
        return jsonify({
            "status": "success",
            "vector_id": vector_id,
            "message": f"Vector {vector_id} activated!"
        })
    
    return jsonify({"status": "error", "message": "Invalid vector or already owned"}), 400

# ============================================================================
# TRADE PROGRAM ENDPOINTS
# ============================================================================

@app.route('/trade/status', methods=['GET'])
def get_trade_status():
    """Returns current trade program status and credits"""
    import datetime
    
    # Calculate days until next payout (first of next month)
    now = datetime.datetime.now()
    next_month = (now.month % 12) + 1
    next_year = now.year if next_month > now.month else now.year + 1
    next_payout = datetime.datetime(next_year, next_month, 1)
    days_until = (next_payout - now).days
    
    return jsonify({
        "active": USER_DATA["trade_active"],
        "credits_this_month": USER_DATA["trade_credits"]["this_month"],
        "total_credits": USER_DATA["trade_credits"]["total_lifetime"],
        "conversations_shared": USER_DATA["trade_credits"]["conversations_shared"],
        "days_until_payout": days_until,
        "value_generated": USER_DATA["trade_credits"]["conversations_shared"] * 0.05  # $0.05 per convo
    })

@app.route('/trade/toggle', methods=['POST'])
def toggle_trade_program():
    """Enable or disable trade program"""
    data = request.json
    active = data.get('active', False)
    
    USER_DATA["trade_active"] = active
    
    return jsonify({
        "status": "success",
        "active": active,
        "message": "Trade program enabled" if active else "Trade program disabled"
    })

@app.route('/trade/calculate', methods=['POST'])
def calculate_trade_credits():
    """Calculate trade credits for current month"""
    # This would run monthly via cron job
    
    # Get user's activity this month
    platforms_used = len(set(
        node.payload.get('platform')
        for node in memory_system.nodes.values()
        if node.payload.get('platform')
    ))
    
    conversation_count = len([
        n for n in memory_system.nodes.values()
        if 'conversation_id' in n.payload
    ])
    
    # Pattern diversity (0-1 score based on crystal variety)
    pattern_diversity = min(1.0, len(crystal_system.crystals) / 100.0)
    
    # Calculate credits: (platforms × conversations × diversity) / 1000
    credits = (platforms_used * conversation_count * pattern_diversity) / 1000
    
    USER_DATA["trade_credits"]["this_month"] = round(credits, 2)
    USER_DATA["trade_credits"]["total_lifetime"] += round(credits, 2)
    USER_DATA["trade_credits"]["conversations_shared"] = conversation_count
    
    return jsonify({
        "credits_earned": round(credits, 2),
        "platforms_used": platforms_used,
        "conversations": conversation_count,
        "diversity_score": round(pattern_diversity, 2)
    })

# ============================================================================
# SHUTDOWN HANDLER
# ============================================================================

def shutdown_trinity():
    """Graceful shutdown of Trinity system"""
    print("\n[CORTEX] Shutting down Trinity...")
    stop_memory_system(save_thread, merge_thread)
    print("[CORTEX] Shutdown complete.")

if __name__ == '__main__':
    try:
        app.run(host='127.0.0.1', port=5000, debug=False)
    except KeyboardInterrupt:
        shutdown_trinity()
