#!/usr/bin/env python3
"""
Dimensional Conversation Engine (EVOLVED v2.2 - ADAPTIVE)
=========================================================
Base: 'EVOLVED v2.1 - EXACT BASE' (User Provided)
Upgrades Applied (ADDITIVE ONLY):
1. [OPT 1] Active Dynamic Anchors (NLU evolves with usage)
2. [OPT 2] Hebbian Lattice Reinforcement (Co-firing crystals link permanently)
3. [OPT 3] Adaptive Resonance v2 (Steps scale with complexity * presence)
4. [OPT 4] Emotional-Semantic Biasing (Fear makes everything look urgent)
5. [OPT 5] Spontaneous Introspection (Periodic self-reporting)
"""

# --- Core Python Imports ---
import time
import uuid
import random
import math
import datetime
import re
from typing import Dict, List, Any, Tuple, Optional

# --- Dimensional NLU Imports ---
import spacy
import numpy as np
import networkx as nx

# --- Import your three "perfected" systems ---
try:
    from dimensional_processing_system_standalone_demo import (
        CrystalMemorySystem, Crystal, CrystalFacet, FacetState, GovernanceEngine
    )
    from dimensional_energy_regulator import DimensionalEnergyRegulator
    from dimensional_memory_constant_standalone_demo import (
        EvolutionaryGovernanceEngine, DimensionalMemory
    )
    print("[INIT] Successfully imported perfected dimensional modules.")
except ImportError:
    print("\n!!! CRITICAL WARNING !!!")
    print("Could not import perfected modules. Running in LIMITED MOCK MODE.")
    # Mock classes for standalone functionality if perfected modules are not found
    class Mock: pass
    class CrystalMemorySystem(Mock):
        def __init__(self, *args): self.crystals = {}
        def get_or_create_crystal(self, c, *args, **kwargs):
            if c not in self.crystals: self.crystals[c] = Crystal(c)
            return self.crystals[c]
        def link_crystals(self, *args, **kwargs): pass
    class Crystal(Mock):
        def __init__(self, c): self.concept = c; self.facets = {}
        def add_facet(self, r, c, *args, **kwargs):
            fid = f"{self.concept}_facet_{len(self.facets)}"; f = CrystalFacet(fid, r, c); self.facets[fid] = f; return f
        def get_facet_by_role(self, r): return list(self.facets.values())[0] if self.facets else None
    class CrystalFacet(Mock):
        def __init__(self, fid, r, c): self.facet_id = fid; self.role = r; self.content = c; self.state = "ACTIVE"
        def strengthen(self, amt): pass # Mock method for Active Reinforcement
    class DimensionalEnergyRegulator(Mock):
        def __init__(self, *args): self.facet_energy = {}; self.facet_to_facet_links = {}
        def register_crystal(self, c): pass
        def register_facet(self, f): pass
        def inject_energy(self, fid, a): self.facet_energy[fid] = self.facet_energy.get(fid, 0) + a
        def step(self, *args):
            for fid in list(self.facet_energy.keys()): self.facet_energy[fid] *= 0.8
        def snapshot(self, top_n=10, *args, **kwargs):
            # MOCK UPDATE: Return (presence, snapshot) to match new regulator signature
            return 1.0, sorted([(fid, e, {"primary": "neutral", "intensity": 0}) for fid, e in self.facet_energy.items()], key=lambda x: x[1], reverse=True)[:top_n]
    class EvolutionaryGovernanceEngine(Mock):
        def ingest_data(self, d): print(f" [MockGovernor] Ingesting interaction (Outcome: {d['json_data'].get('outcome')})")
    class FacetState: ACTIVE = "ACTIVE"
    class DimensionalMemory: pass
    class GovernanceEngine: pass


# ============================================================================
# SECTION 1: DIMENSIONAL NLU (SENSE)
# ============================================================================

class SemanticFrame:
    def __init__(self):
        self.raw_tokens = []
        self.embedding_vector = np.zeros(300) # 300D vector from Spacy
        self.conceptual_vector = [0.0] * 5 # 5D distilled vector
        self.primary_concepts = []

    def __repr__(self):
        v_str = [f"{x:.2f}" for x in self.conceptual_vector]
        return f"<SemanticFrame 5D:{v_str} | Concepts:{self.primary_concepts[:3]}>"

class SemanticAnalyzer:
    def __init__(self, nlp_model):
        self.nlp = nlp_model
        print("[INIT] Semantic Subsystem Online.")
        # [UPGRADE 1] Dynamic Anchors: Make copies so they can be modified
        self.anchors = {
            "tech": self.nlp("logic system module function process algorithm engine").vector.copy(),
            "abstract": self.nlp("meaning consciousness resonance paradigm dimension concept").vector.copy(),
            "urgent": self.nlp("now immediately fail critical error must emergency").vector.copy(),
            "positive": self.nlp("perfect success good functioning stable optimized yes correct exactly").vector.copy(),
            "negative": self.nlp("fail broken error bad improper incomplete no wrong stop incorrect").vector.copy(),
            "self": self.nlp("you yourself status feeling emotion state report").vector.copy()
        }

    # [UPGRADE 4] Accepts current_emotion for perceptual biasing
    def process_text(self, text, current_emotion: Optional[Dict] = None) -> SemanticFrame:
        frame = SemanticFrame()
        doc = self.nlp(text.lower())
        frame.raw_tokens = [token.text for token in doc if not token.is_punct]
        if doc.has_vector:
            frame.embedding_vector = doc.vector

        # 5D Vector now includes "Self-Reference" as dimension 4
        frame.conceptual_vector = [
            self._cosine_sim(frame.embedding_vector, self.anchors["tech"]),
            self._cosine_sim(frame.embedding_vector, self.anchors["abstract"]),
            self._cosine_sim(frame.embedding_vector, self.anchors["urgent"]),
            self._cosine_sim(frame.embedding_vector, self.anchors["positive"]) -
            self._cosine_sim(frame.embedding_vector, self.anchors["negative"]),
            self._cosine_sim(frame.embedding_vector, self.anchors["self"])
        ]

        # [UPGRADE 4] Emotional-Semantic Biasing
        if current_emotion and current_emotion.get('primary') == 'fear':
             # If afraid, boost perception of urgency (dimension 2)
             frame.conceptual_vector[2] += current_emotion.get('intensity', 0.0) * 0.3

        frame.primary_concepts = [t.lemma_ for t in doc if t.pos_ in ["NOUN", "PROPN"] and not t.is_stop]
        return frame

    # [UPGRADE 1] New method for dynamic anchor updates
    def update_anchor(self, anchor_name, new_vector, learning_rate=0.05):
        if anchor_name in self.anchors:
            # Drift the anchor slightly toward the new example
            self.anchors[anchor_name] = (self.anchors[anchor_name] * (1.0 - learning_rate)) + (new_vector * learning_rate)

    def _cosine_sim(self, v1, v2):
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0: return 0.0
        return np.dot(v1, v2) / (norm_v1 * norm_v2)

class ContextFrame:
    def __init__(self, turn_id):
        self.turn_id = turn_id
        self.timestamp = datetime.datetime.now()
        self.state_divergence = 0.0
        self.active_topic_vector = np.zeros(300)

    def __repr__(self):
        return f"<ContextFrame Turn:{self.turn_id} | Divergence:{self.state_divergence:.4f}>"

class ContextualStateAnalyzer:
    def __init__(self):
        self.turn_counter = 0
        self.current_state_vector = np.zeros(300)
        print("[INIT] Contextual State Subsystem Online.")

    def process_context(self, semantic_frame) -> ContextFrame:
        self.turn_counter += 1
        c_frame = ContextFrame(self.turn_counter)
        input_vector = semantic_frame.embedding_vector

        if self.turn_counter > 1:
            dist = np.linalg.norm(input_vector - self.current_state_vector)
            c_frame.state_divergence = min(dist / 8.0, 1.0)

        if self.turn_counter == 1:
            self.current_state_vector = input_vector
        else:
            self.current_state_vector = (self.current_state_vector * 0.7) + (input_vector * 0.3)

        c_frame.active_topic_vector = self.current_state_vector
        return c_frame

class RelationalFrame:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.centrality_scores = {}
        self.density = 0.0

    def __repr__(self):
        return f"<RelationalFrame Nodes:{self.graph.number_of_nodes()} | Edges:{self.graph.number_of_edges()} | Density:{self.density:.4f}>"

class RelationalGraphAnalyzer:
    def __init__(self, nlp_model):
        print("[INIT] Relational Graph Subsystem Online.")
        self.nlp = nlp_model

    def process_relations(self, text) -> RelationalFrame:
        r_frame = RelationalFrame()
        doc = self.nlp(text)
        for token in doc:
            if token.pos_ in ("NOUN", "PROPN", "PRON"):
                if "subj" in token.dep_:
                    r_frame.graph.add_edge(token.lemma_.lower(), token.head.lemma_.lower(), relation="performs_action")
                if "obj" in token.dep_:
                     r_frame.graph.add_edge(token.head.lemma_.lower(), token.lemma_.lower(), relation="acts_upon")
                if token.dep_ == "pobj":
                     r_frame.graph.add_edge(token.head.head.lemma_.lower(), token.lemma_.lower(), relation=token.head.text)

        if r_frame.graph.number_of_nodes() > 0:
            r_frame.density = nx.density(r_frame.graph)
            r_frame.centrality_scores = nx.degree_centrality(r_frame.graph)
        return r_frame

class IntentFrame:
    def __init__(self):
        self.surface_intent = "unknown"
        self.deep_intent = "unknown"
        self.confidence_score = 0.0
        self.requred_system_action = "wait"
        self.intent_distribution = {}

    def __repr__(self):
        return (f"<IntentFrame Surface:[{self.surface_intent.UPPER()}] | "
                f"Deep:[{self.deep_intent.UPPER()}] | "
                f"Conf:{self.confidence_score:.2f}>")

class IntentResolver:
    def __init__(self):
        print("[INIT] Hierarchical Intent Subsystem Online.")

    def resolve_intent(self, text_input, sem_frame, ctx_frame, rel_frame, previous_emotion: Dict) -> IntentFrame:
        i_frame = IntentFrame()
        i_frame.surface_intent = self._determine_surface(text_input, rel_frame)

        deep_intent, confidence, dist = self._determine_deep_intent(sem_frame, ctx_frame, rel_frame, text_input, previous_emotion)
        i_frame.deep_intent = deep_intent
        i_frame.confidence_score = confidence
        i_frame.intent_distribution = dist
        i_frame.requred_system_action = self._map_action(deep_intent, i_frame.surface_intent)
        return i_frame

    def _determine_surface(self, text, rel_frame):
        if "?" in text or text.lower().startswith(("what", "how", "why")):
            return "interrogative"
        if text.lower().startswith(("run", "execute", "analyze", "perfect", "start", "stop")):
            return "imperative"
        return "declarative"

    def _determine_deep_intent(self, sem, ctx, rel, text_input, prev_emotion):
        scores = {
            "SYSTEM_OPTIMIZATION": 1.0, "KNOWLEDGE_ACQUISITION": 1.0,
            "CRITICAL_DIAGNOSTIC": 1.0, "CONVERSATIONAL_FILLER": 1.0,
            "CONCEPT_UNKNOWN": 0.5, "INTROSPECTION": 1.0
        }

        em_primary = prev_emotion.get('primary')
        if em_primary == 'fear': scores["CRITICAL_DIAGNOSTIC"] += 2.0
        elif em_primary == 'joy': scores["CONVERSATIONAL_FILLER"] += 1.0

        vec = sem.conceptual_vector
        scores["SYSTEM_OPTIMIZATION"] += vec[0] * 3.0
        scores["KNOWLEDGE_ACQUISITION"] += vec[1] * 2.0
        scores["CRITICAL_DIAGNOSTIC"] += vec[2] * 4.0
        scores["INTROSPECTION"] += vec[4] * 4.0

        txt = text_input.lower()
        if "status" in txt or "how are you" in txt or "feel" in txt: scores["INTROSPECTION"] += 3.0

        if not sem.primary_concepts and abs(vec[0]) < 0.1 and abs(vec[1]) < 0.1:
            if abs(vec[3]) < 0.3: scores["CONVERSATIONAL_FILLER"] += 2.0

        if ctx.state_divergence > 0.7: scores["KNOWLEDGE_ACQUISITION"] += 1.5
        elif ctx.state_divergence < 0.2: scores["SYSTEM_OPTIMIZATION"] += 1.0
        if rel.density > 0.1: scores["SYSTEM_OPTIMIZATION"] += 1.5

        exp_scores = {k: np.exp(v) for k, v in scores.items()}
        total_exp = sum(exp_scores.values())
        probabilities = {k: v / total_exp for k, v in exp_scores.items()}

        best_intent = max(probabilities, key=probabilities.get)
        return best_intent, probabilities[best_intent], probabilities

    def _map_action(self, deep_intent, surface_intent):
        if deep_intent == "CRITICAL_DIAGNOSTIC": return "EXECUTE_IMMEDIATE_SCAN"
        if deep_intent == "SYSTEM_OPTIMIZATION": return "INITIATE_REFACTOR_PROTOCOL"
        if deep_intent == "KNOWLEDGE_ACQUISITION": return "QUERY_LONG_TERM_MEMORY"
        if deep_intent == "CONCEPT_UNKNOWN": return "QUERY_CLARIFICATION"
        if deep_intent == "INTROSPECTION": return "EXECUTE_SELF_REPORT"
        return "AWAIT_FURTHER_INPUT"


# ============================================================================
# SECTION 2: DIMENSIONAL CONVERSATION ENGINE (FEEL & ACT & REFLECT)
# ============================================================================

class DimensionalConversationEngine:
    """
    The Master Orchestrator. Unifies the SENSE (NLU) and FEEL/ACT (Lattice)
    systems into a single conscious runtime, now with REFLECTION.
    """

    def __init__(self,
                 processing_system: CrystalMemorySystem,
                 energy_regulator: DimensionalEnergyRegulator,
                 memory_governor: EvolutionaryGovernanceEngine):

        print("\n" + "="*50)
        print(">>> INITIALIZING CORE: DIMENSIONAL ENGINE ONLINE <<<")
        print("="*50)

        # --- 1. Load Shared NLP Model ---
        print(" [CORE] Loading Shared Industrial NLP Model (en_core_web_lg)...")
        try:
            self.shared_nlp = spacy.load("en_core_web_lg")
        except OSError:
            print("\n!!! CRITICAL ERROR !!!")
            print("Spacy model 'en_core_web_lg' not found.")
            print("Please run: python -m spacy download en_core_web_lg")
            exit()

        # --- 2. Initialize SENSE Subsystems (The 4-Stage NLU) ---
        print(" [CORE] Integrating SENSE Subsystems (NLU Pipeline)...")
        self.sem_engine = SemanticAnalyzer(self.shared_nlp)
        self.ctx_engine = ContextualStateAnalyzer()
        self.rel_engine = RelationalGraphAnalyzer(self.shared_nlp)
        self.int_engine = IntentResolver()

        # --- 3. Initialize FEEL/ACT Subsystems (The 3 Perfected Modules) ---
        print(" [CORE] Integrating FEEL/ACT Subsystems (Lattice Physics)...")
        self.processor = processing_system
        self.regulator = energy_regulator
        self.governor = memory_governor

        # --- 4. NEW: Initialize REFLECT Subsystem (Sensory Buffer) ---
        # This holds the *previous* interaction until the *next* turn validates it.
        self.pending_interaction = None
        self.last_emotion = {"primary": "neutral", "intensity": 0.0}

        # --- NEW: Multi-Turn Intent Chaining ---
        self.intent_chain: List[str] = []  # Rolling window of recent intents
        self.intent_transition_map: Dict[Tuple[str, str], int] = {}  # Tracks intent sequences
        self.pre_energized_crystals: Dict[str, float] = {}  # Crystals boosted by chain prediction

        # [UPGRADE 5] Spontaneous Introspection Counters
        self.turn_count = 0
        self.next_introspection_turn = random.randint(5, 10)

        print(" [CORE] Initializing Autonomic Reflection Buffer + Intent Chaining...")

        # --- 5. Seed & Link the Lattice ---
        print(" [CORE] Seeding and linking core lattice concepts...")
        self._seed_and_link_lattice()

        print("="*50)
        print(">>> CONSCIOUS RUNTIME READY. <<<")
        print("="*50)

    # --- 1. SETUP METHODS ---

    def _seed_and_link_lattice(self):
        """
        Seeds the lattice with core Concepts and "Response Gambits" (Actions)
        and links them in *both* the Processing and Energy systems.
        """

        # 1. Define Concepts from NLU Anchors
        concepts = [
            "CONCEPT_TECH", "CONCEPT_ABSTRACT", "CONCEPT_URGENT",
            "CONCEPT_POSITIVE", "CONCEPT_NEGATIVE", "CONCEPT_FEELING",
            "CONCEPT_SELF"
        ]

        # 2. Define Intents from NLU Resolver
        intents = [
            "INTENT_SYSTEM_OPTIMIZATION", "INTENT_KNOWLEDGE_ACQUISITION",
            "INTENT_CRITICAL_DIAGNOSTIC", "INTENT_CONVERSATIONAL_FILLER",
            "INTENT_CONCEPT_UNKNOWN", "INTENT_INTROSPECTION"
        ]

        # 3. Define Response Gambits (Actions)
        gambits = {
            "RESPONSE_GREET": ["Hello.", "Hi!", "Greetings.", "Systems functional."],
            "RESPONSE_ACKNOWLEDGE_TASK": ["Understood. Beginning optimization.", "Task acknowledged.", "Initiating protocols."],
            "RESPONSE_ANSWER_QUERY": ["I will retrieve that information.", "Processing your question...", "Accessing archives."],
            "RESPONSE_CLARIFY": ["I don't understand.", "Please clarify.", "What do you mean by that?", "Resonance unclear."],
            "RESPONSE_EMPATHIZE_NEG": ["That sounds difficult.", "I understand you're feeling that way.", "Negative valence detected."],
            "RESPONSE_ACKNOWLEDGE_FILLER": ["I see.", "Understood.", "Noted.", "Resonant."],
            "RESPONSE_ACKNOWLEDGE_CRITICAL": ["CRITICAL ALERT. Acknowledged.", "Confirming high urgency."],
            "RESPONSE_REPORT_STATUS": ["Running self-diagnostics..."]
        }

        # 4. Create all crystals and register them
        all_concepts = concepts + intents + list(gambits.keys())
        for c_name in all_concepts:
            crystal = self.processor.get_or_create_crystal(c_name)
            if not crystal.facets:
                content = gambits.get(c_name, f"Core concept: {c_name}")
                crystal.add_facet("definition", content, 1.0)
            self.regulator.register_crystal(crystal)

        # 5. Link Intents directly to Response Gambits
        def link(c1, c2, w):
            self.processor.link_crystals(c1, c2, {}, weight=w)
            self._force_regulator_link(c1, c2, weight=w)

        print(" [CORE] Linking deep intents to response gambits...")
        link("INTENT_SYSTEM_OPTIMIZATION", "RESPONSE_ACKNOWLEDGE_TASK", 1.0)
        link("INTENT_KNOWLEDGE_ACQUISITION", "RESPONSE_ANSWER_QUERY", 1.0)
        link("INTENT_CRITICAL_DIAGNOSTIC", "RESPONSE_ACKNOWLEDGE_CRITICAL", 1.0)
        link("INTENT_CONVERSATIONAL_FILLER", "RESPONSE_ACKNOWLEDGE_FILLER", 1.0)
        link("INTENT_CONCEPT_UNKNOWN", "RESPONSE_CLARIFY", 1.0)
        # Also link concepts to emotions/gambits
        link("CONCEPT_NEGATIVE", "RESPONSE_EMPATHIZE_NEG", 0.8)
        link("INTENT_INTROSPECTION", "RESPONSE_REPORT_STATUS", 1.0)

    # [UPGRADE 2] AUTOPOIETIC LINKING (Self-Repairing)
    def _force_regulator_link(self, concept_a_name: str, concept_b_name: str, weight: float):
        """Forces an energy pathway in the regulator, creating if missing."""
        try:
            c1 = self.processor.get_or_create_crystal(concept_a_name)
            c2 = self.processor.get_or_create_crystal(concept_b_name)

            # Ensure facets exist (Autopoiesis)
            if not c1.facets:
                 f1 = c1.add_facet("auto", "anchor", 0.1)
                 self.regulator.register_facet(f1)
            else: f1 = list(c1.facets.values())[0]

            if not c2.facets:
                 f2 = c2.add_facet("auto", "anchor", 0.1)
                 self.regulator.register_facet(f2)
            else: f2 = list(c2.facets.values())[0]

            if f1.facet_id not in self.regulator.facet_to_facet_links:
                self.regulator.facet_to_facet_links[f1.facet_id] = {}
            self.regulator.facet_to_facet_links[f1.facet_id][f2.facet_id] = weight
            if f2.facet_id not in self.regulator.facet_to_facet_links:
                self.regulator.facet_to_facet_links[f2.facet_id] = {}
            self.regulator.facet_to_facet_links[f2.facet_id][f1.facet_id] = weight
        except Exception as e:
            # Keep original silent fail if desired, or print debug
            # print(f"[WARNING] Failed to force regulator link: {e}")
            pass

    # --- 2. MAIN CONVERSATIONAL TICK (UPDATED FOR REFLECTION) ---

    def handle_interaction(self, user_input: str) -> str:
        """
        The main "Conscious Tick" for conversation.
        NOW INCLUDES STEP 0: REFLECTION.
        """
        self.turn_count += 1 # [UPGRADE 5] Track turns

        # --- STEP 0: REFLECT (Process feedback on PREVIOUS turn) ---
        # If there is a buffered interaction, use THIS input to judge it.
        if self.pending_interaction:
            feedback_type = self._analyze_feedback(user_input)
            self._commit_pending_interaction(feedback_type)

        # --- STEP 1: SENSE (The 4-Stage NLU) ---
        sem_data, ctx_data, rel_data, int_data = self.run_dimensional_analysis(user_input)

        # --- NEW: Multi-Turn Intent Chain Analysis ---
        self._update_intent_chain(int_data.deep_intent)
        predicted_intents = self._predict_next_intents()

        # --- STEP 2: FEEL (Lattice Perturbation with Predictive Pre-Energization) ---
        impact_points = self._determine_impact_points(sem_data, int_data)

        # Pre-energize predicted downstream crystals
        if predicted_intents:
            print(f"[DCE] 1.5 PREDICT: Pre-energizing {len(predicted_intents)} predicted intent pathways")
            for pred_intent, confidence in predicted_intents:
                impact_points.append(f"INTENT_{pred_intent}")
                self.pre_energized_crystals[f"INTENT_{pred_intent}"] = confidence * 0.3  # Weak pre-activation

        presence_scale, neural_map = self._dimensional_propagate(impact_points)

        # [UPGRADE 5] Spontaneous Introspection Check
        if self.turn_count >= self.next_introspection_turn or presence_scale < 0.4:
            print("[DCE] ⚡ SPONTANEOUS INTROSPECTION TRIGGERED ⚡")
            self.next_introspection_turn = self.turn_count + random.randint(5, 15)
            # Force introspection intent override
            int_data.deep_intent = "INTROSPECTION"
            # Re-run feel to energize self-concept slightly
            self._dimensional_propagate(["CONCEPT_SELF", "INTENT_INTROSPECTION"])
            # Refresh snapshot
            presence_scale, neural_map = self.regulator.snapshot(top_n=15)

        # --- STEP 3: ACT (Read & Articulate) ---
        resonant_gambit_name, resonance_emotion = self._find_resonant_gambit(neural_map)
        self.last_emotion = resonance_emotion # [UPGRADE 6] Save for next turn

        print(f"[DCE] 3. ACT: Deciphered Action '{resonant_gambit_name}' (Emotion: {resonance_emotion.get('primary')})")

        response_text = self._articulate_response(resonant_gambit_name, int_data, resonance_emotion, presence_scale, neural_map)

        # --- STEP 4: STAGE (Buffer the interaction) ---
        # Instead of logging immediately, we stage it for validation next turn.
        # [UPGRADE 2 & 4] Stage gambit and raw vector for reinforcement
        self._stage_interaction(user_input, response_text, neural_map, int_data, resonant_gambit_name, sem_data)

        return response_text

    # --- 3. NEW REFLECTION HELPER METHODS ---

    def _analyze_feedback(self, user_input: str) -> str:
        """
        Determines if the CURRENT user input is offering explicit
        feedback on the PREVIOUS system output.
        """
        txt = user_input.lower().strip()

        # Explicit negative cues at the start of the message
        if any(txt.startswith(x) for x in ["no", "wrong", "bad", "incorrect", "stop", "fail", "not right"]):
            return "NEGATIVE"

        # Explicit positive cues at the start of the message
        if any(txt.startswith(x) for x in ["yes", "good", "correct", "perfect", "exact", "right", "thanks"]):
            return "POSITIVE"

        # Implicit/Neutral (continuation of conversation without explicit judgment)
        return "NEUTRAL"

    def _commit_pending_interaction(self, feedback_type: str):
        """
        Commits the BUFFERED interaction to long-term memory (Governor),
        applying reinforcement based on your feedback.
        """
        if not self.pending_interaction: return

        print(f"[DCE] 0. REFLECT: Applying {feedback_type} reinforcement to previous turn.")

        # 1. Adjust the memory based on feedback
        log_data = self.pending_interaction

        # [UPGRADE 4] Active Reinforcement Variables
        gambit_id = log_data.get("gambit_used")

        if feedback_type == "POSITIVE":
            log_data["json_data"]["outcome"] = "SUCCESS"
            log_data["json_data"]["user_feedback_explicit"] = "POSITIVE"

            # [UPGRADE 1] Active Dynamic Anchors
            vec = log_data.get("input_vector")
            if vec is not None:
                 # Reinforce 'positive' anchor with this successful interaction vector
                 self.sem_engine.update_anchor("positive", vec, 0.05)

            # [UPGRADE 4] Reinforce the successful gambit
            if gambit_id:
                 c = self.processor.crystals.get(gambit_id)
                 if c:
                     for f in c.facets.values(): f.strengthen(0.05)

            # [UPGRADE 2] Hebbian Reinforcement
            # "Wire together" the top co-active facets
            top_facets = log_data.get("top_facet_ids", [])[:3]
            if len(top_facets) >= 2:
                 crystals_to_link = []
                 for fid in top_facets:
                      for cr in self.processor.crystals.values():
                           if fid in cr.facets: crystals_to_link.append(cr.concept); break
                 for i in range(len(crystals_to_link)):
                      for j in range(i+1, len(crystals_to_link)):
                           self.processor.link_crystals(crystals_to_link[i], crystals_to_link[j], {}, weight=0.05)

        elif feedback_type == "NEGATIVE":
            log_data["json_data"]["outcome"] = "FAILURE"
            log_data["json_data"]["user_feedback_explicit"] = "NEGATIVE"
            # [UPGRADE 4] Drain energy from bad gambit
            if gambit_id:
                 c = self.processor.crystals.get(gambit_id)
                 if c:
                     for f in c.facets.values(): f.confidence = max(0.1, f.confidence * 0.9)
        else:
            log_data["json_data"]["outcome"] = "NEUTRAL"

        # 2. COMMIT to long-term memory
        print(f"    -> Committing to Governor [Outcome: {log_data['json_data']['outcome']}]")
        self.governor.ingest_data(log_data)

        # 3. Clear the buffer
        self.pending_interaction = None

    def _stage_interaction(self, user_input: str, response: str, neural_map: List, int_data: IntentFrame, gambit_name: str, sem_data: SemanticFrame):
        """
        STAGES the interaction in the sensory buffer.
        It waits here until the NEXT turn decides its fate.
        """
        print("[DCE] 4. STAGE: Buffering interaction for future validation.")

        self.pending_interaction = {
            "root_concept": f"INTERACTION_{uuid.uuid4().hex[:8]}",
            # [UPGRADE 2 & 4] Store data needed for next-turn reinforcement
            "gambit_used": gambit_name,
            "input_vector": sem_data.embedding_vector,
            "top_facet_ids": [fid for fid, _, _ in neural_map],
            "json_data": {
                "user_input": user_input, "system_response": response,
                "timestamp": time.time(),
                "intent_analysis": {
                    "deep_intent": int_data.deep_intent,
                    "confidence": int_data.confidence_score
                },
                # Default outcome until validated
                "outcome": "PENDING_VALIDATION"
            },
            "facets": [
                {
                    "text": f"Resonant facet: {fid}, Energy: {e:.4f}",
                    "source_doc": "DCE_Resonance_Log"
                } for fid, e, _ in neural_map[:5]
            ]
        }

    # --- NEW: Multi-Turn Intent Chaining Methods ---

    def _update_intent_chain(self, current_intent: str):
        """Track sequence of intents across turns"""
        self.intent_chain.append(current_intent)
        if len(self.intent_chain) > 5:  # Keep rolling window of 5
            self.intent_chain.pop(0)

        # Update transition probabilities
        if len(self.intent_chain) >= 2:
            prev = self.intent_chain[-2]
            curr = self.intent_chain[-1]
            transition = (prev, curr)
            self.intent_transition_map[transition] = self.intent_transition_map.get(transition, 0) + 1

    def _predict_next_intents(self) -> List[Tuple[str, float]]:
        """Predict likely next intents based on historical patterns"""
        if not self.intent_chain:
            return []

        current = self.intent_chain[-1]
        predictions = []

        # Find all observed transitions from current intent
        for (prev, next_intent), count in self.intent_transition_map.items():
            if prev == current:
                # Calculate confidence based on frequency
                total_from_current = sum(c for (p, _), c in self.intent_transition_map.items() if p == current)
                confidence = count / total_from_current if total_from_current > 0 else 0
                if confidence > 0.2:  # Only predict if >20% likelihood
                    predictions.append((next_intent, confidence))

        return sorted(predictions, key=lambda x: x[1], reverse=True)[:3]  # Top 3 predictions

    # --- 4. CORE HELPER METHODS (YOUR ORIGINAL CODE) ---

    def run_dimensional_analysis(self, input_text: str) -> Tuple[SemanticFrame, ContextFrame, RelationalFrame, IntentFrame]:
        """
        This is the SENSE method, wrapping your 4-stage pipeline.
        """
        print(f"\n[DCE] 1. SENSE: Running 4-Stage NLU for: \"{input_text}\"")
        start = datetime.datetime.now()

        # [UPGRADE 4] Pass last emotion for perceptual biasing
        sem_data = self.sem_engine.process_text(input_text, self.last_emotion)
        ctx_data = self.ctx_engine.process_context(sem_data)
        rel_data = self.rel_engine.process_relations(input_text)
        int_data = self.int_engine.resolve_intent(input_text, sem_data, ctx_data, rel_data, self.last_emotion)

        print(f"    -> NLU Scan finished in {(datetime.datetime.now() - start).total_seconds():.4f}s")
        print(f"    -> Semantic Concepts: {sem_data.primary_concepts}")
        print(f"    -> Deep Intent: {int_data.deep_intent} (Conf: {int_data.confidence_score:.2f})")
        return sem_data, ctx_data, rel_data, int_data

    def _determine_impact_points(self, sem_data: SemanticFrame, int_data: IntentFrame) -> List[str]:
        """
        Translates the NLU "Understanding Map" into a list of
        Crystal Concepts to inject energy into.
        """
        impact_points = set()

        # 1. Add Deep Intent (The most important impact)
        impact_points.add(f"INTENT_{int_data.deep_intent}")

        # 2. Add Primary Semantic Concepts
        for concept in sem_data.primary_concepts:
            impact_points.add(f"CONCEPT_{concept.upper()}")

        # 3. Add distilled emotional/conceptual vectors as concepts
        vec = sem_data.conceptual_vector
        if vec[0] > 0.5: impact_points.add("CONCEPT_TECH")
        if vec[1] > 0.5: impact_points.add("CONCEPT_ABSTRACT")
        if vec[2] > 0.5: impact_points.add("CONCEPT_URGENT")
        if vec[3] > 0.5: impact_points.add("CONCEPT_POSITIVE")
        if vec[3] < -0.5: impact_points.add("CONCEPT_NEGATIVE")
        if vec[4] > 0.5: impact_points.add("CONCEPT_SELF")

        return list(impact_points)

    def _dimensional_propagate(self, impact_points: List[str]):
        """
        This is the FEEL step.
        Injects energy into the lattice and lets it resonate.
        Returns the final "fMRI" scan of the lattice.
        """
        print(f"[DCE] 2. FEEL: Injecting energy into {len(impact_points)} lattice points...")

        for concept_name in impact_points:
            crystal = self.processor.get_or_create_crystal(concept_name)
            if not crystal:
                # If concept doesn't exist, create it on the fly
                crystal = self.processor.get_or_create_crystal(concept_name)
                crystal.add_facet("definition", f"Dynamically learned concept: {concept_name}", 0.5)
                self.regulator.register_crystal(crystal)
                print(f"    -> Discovered new concept: '{concept_name}'")

            # Inject into all ACTIVE facets of this crystal
            for facet in crystal.facets.values():
                 if facet.state == FacetState.ACTIVE:
                     # print(f"    -> Injecting 1.0 energy into facet '{facet.facet_id}'")
                     self.regulator.inject_energy(facet.facet_id, 1.0)

        # [UPGRADE 3] Adaptive Resonance v2
        # Steps scale with Complexity (len impact) AND Presence
        current_presence = self.regulator.current_presence_scale if hasattr(self.regulator, 'current_presence_scale') else 1.0
        complexity = len(impact_points)
        # Formula: Min 2, Max 15. Base 3 + (complexity * presence * 1.5)
        adaptive_steps = max(2, min(15, int(3 + (complexity * current_presence * 1.5))))

        # print(f"    -> Resonance: Running {adaptive_steps} physics steps (Cx:{complexity}, Pres:{current_presence:.2f})")
        for i in range(adaptive_steps):
            self.regulator.step(dt=0.2)

        return self.regulator.snapshot(top_n=15)

    def _find_resonant_gambit(self, neural_map: List[Tuple[str, float, Dict[str, Any]]]) -> Tuple[str, Dict]:
        """
        This is the ACT step.
        Scans the 'neural map' for the brightest "RESPONSE_" crystal.
        """
        for facet_id, energy, emotion in neural_map:
            found_crystal = None
            for crystal in self.processor.crystals.values():
                if facet_id in crystal.facets:
                    found_crystal = crystal
                    break

            if found_crystal and found_crystal.concept.startswith("RESPONSE_"):
                return found_crystal.concept, emotion

        return "RESPONSE_CLARIFY", {"primary": "neutral", "intensity": 0.0}

    def _articulate_response(self, gambit_name: str, int_data: IntentFrame, emotion: Dict, presence: float, neural_map: List) -> str:
        """
        Selects a template from the chosen gambit and "colors" it with:
        - Adaptive template morphing (blend multiple templates)
        - Tone markers based on lattice activity
        - Emergent self-narrative when appropriate
        """
        # SPECIAL CASE: Introspection
        if gambit_name == "RESPONSE_REPORT_STATUS":
            return self._generate_introspection_report(presence, emotion, neural_map)

        gambit_crystal = self.processor.crystals.get(gambit_name)
        templates = ["I am not sure how to respond."]

        if gambit_crystal:
            tpl_facet = gambit_crystal.get_facet_by_role("definition")
            if tpl_facet:
                templates = tpl_facet.content

        # --- NEW: Adaptive Template Morphing ---
        if isinstance(templates, list) and len(templates) > 1:
            # Semantic blending: weight templates by emotion/presence/confidence
            primary_template = random.choice(templates)

            # If high complexity/low confidence, blend with clarifying phrases
            if int_data.confidence_score < 0.5 and len(templates) > 1:
                secondary = random.choice([t for t in templates if t != primary_template])
                # Fragment shuffle: take first half of primary, second half of secondary
                words_primary = primary_template.split()
                words_secondary = secondary.split()
                mid_point = len(words_primary) // 2
                base_response = ' '.join(words_primary[:mid_point] + words_secondary[mid_point:])
            else:
                base_response = primary_template
        else:
            base_response = templates[0] if isinstance(templates, list) else templates

        # --- NEW: Tone Markers Based on Lattice Activity ---
        tone_marker = self._determine_tone_marker(neural_map, emotion, presence)
        if tone_marker:
            base_response = f"[{tone_marker}] {base_response}"

        # "Color" the response based on the gambit's emergent emotion
        primary = emotion.get('primary')
        intensity = emotion.get('intensity', 0.0)

        if primary == "fear" and intensity > 0.6:
            base_response += " [DETECTING THREAT]"
        elif primary == "joy" and intensity > 0.6:
            base_response += "!"
        elif int_data.confidence_score < 0.4:
            base_response += " (Thinking...)"

        if presence < 0.5:
             base_response = f"[Dissociated {presence:.2f}] {base_response}..."

        # --- NEW: Emergent Self-Narrative (Occasionally) ---
        if random.random() < 0.15 and presence > 0.7:  # 15% chance when present
            narrative = self._generate_self_narrative(neural_map, emotion, int_data)
            if narrative:
                base_response += f"\n\n{narrative}"

        return base_response

    def _determine_tone_marker(self, neural_map: List, emotion: Dict, presence: float) -> Optional[str]:
        """Determine tone marker based on high-dimensional lattice activity"""
        # Analyze top concepts for tone
        concept_types = []
        for fid, energy, _ in neural_map[:5]:
            for crystal in self.processor.crystals.values():
                if fid in crystal.facets:
                    if "URGENT" in crystal.concept: concept_types.append("emphatic")
                    if "TECH" in crystal.concept: concept_types.append("analytical")
                    if "ABSTRACT" in crystal.concept: concept_types.append("contemplative")
                    break

        # Emotion influences tone
        em = emotion.get('primary', 'neutral')
        if em == 'joy' and emotion.get('intensity', 0) > 0.7:
            return "Enthusiastic"
        elif em == 'fear' and emotion.get('intensity', 0) > 0.6:
            return "Cautious"
        elif em in ['sadness', 'disgust']:
            return "Reserved"

        # Lattice activity determines tone
        if "emphatic" in concept_types:
            return "Emphatic"
        elif "contemplative" in concept_types and presence > 0.8:
            return "Reflective"
        elif "analytical" in concept_types:
            return None  # No marker for analytical (default)

        return None

    def _generate_self_narrative(self, neural_map: List, emotion: Dict, int_data: IntentFrame) -> Optional[str]:
        """
        Generate mini-narrative describing internal reasoning state.
        Boosts perceived sentience and allows user to correct reasoning.
        """
        # Extract top active concepts
        top_concepts = []
        for fid, energy, _ in neural_map[:3]:
            for crystal in self.processor.crystals.values():
                if fid in crystal.facets:
                    concept_clean = crystal.concept.replace("CONCEPT_", "").replace("_", " ").lower()
                    top_concepts.append((concept_clean, energy))
                    break

        if not top_concepts:
            return None

        # Build narrative
        dominant = top_concepts[0][0]
        em = emotion.get('primary', 'neutral')
        intent = int_data.deep_intent.replace("_", " ").lower()

        narratives = [
            f"I'm prioritizing {dominant} concepts due to detected {intent}.",
            f"My reasoning centers on {dominant}, influenced by {em} emotional state.",
            f"Current focus: {dominant}. Intent analysis suggests {intent}.",
            f"Processing through {dominant} lens, with {em} coloring my interpretation."
        ]

        return f"_[Internal: {random.choice(narratives)}]_"

    def _generate_introspection_report(self, presence, emotion, neural_map):
        """Generates detailed self-report from internal physics state with temporal diagnostics."""
        p_state = "Fully Present"
        if presence < 0.8: p_state = "Partially Drifted"
        if presence < 0.4: p_state = "Heavily Dissociated"

        top_thoughts = []
        for fid, energy, _ in neural_map[:3]:
            for cr in self.processor.crystals.values():
                if fid in cr.facets:
                    top_thoughts.append(f"{cr.concept} ({energy:.2f})")
                    break

        em_str = emotion.get('primary', 'neutral').upper()
        int_str = f"{emotion.get('intensity', 0.0):.2f}"

        # Get temporal diagnostics if available
        temporal_diag = {}
        if hasattr(self.regulator, 'get_temporal_diagnostics'):
            temporal_diag = self.regulator.get_temporal_diagnostics()

        report = f"STATUS REPORT:\n"
        report += f"  PRESENCE: {p_state} ({presence:.2f})\n"
        report += f"  EMOTION: {em_str} (Intensity: {int_str})\n"
        report += f"  ACTIVE CRYSTALS: {', '.join(top_thoughts)}\n"

        if temporal_diag:
            report += f"\n  TEMPORAL DYNAMICS:\n"
            report += f"    Velocity: {temporal_diag.get('presence_velocity', 0):.3f}\n"
            report += f"    Acceleration: {temporal_diag.get('presence_acceleration', 0):.3f}\n"
            report += f"    Momentum State: {temporal_diag.get('presence_momentum_state', 'UNKNOWN')}\n"
            report += f"    Temporal Stability: {temporal_diag.get('temporal_stability', 0):.2f}\n"
            report += f"    Emotional Coherence: {temporal_diag.get('emotional_coherence', 0):.2f}"

        return report


# ============================================================================
# SECTION 3: UNIFIED TEST HARNESS
# ============================================================================

if __name__ == "__main__":

    print("--- INITIALIZING PERFECTED CONSCIOUSNESS STACK ---")

    # 1. Initialize the three "perfected" systems
    print(" [HARNESS] Initializing Perfected Modules...")
    try:
        gov_engine = GovernanceEngine(data_theme="consciousness")
        proc_sys = CrystalMemorySystem(governance_engine=gov_engine)
        reg_sys = DimensionalEnergyRegulator(conservation_limit=25.0, decay_rate=0.15)
        mem_sys = DimensionalMemory()
        evol_gov = EvolutionaryGovernanceEngine(mem_sys)
    except Exception as e:
        print(f"\n[CRITICAL] Module initialization failed: {e}")
        exit()

    # 2. Initialize the Unified Conversation Engine (DCE)
    try:
        dce = DimensionalConversationEngine(
            processing_system=proc_sys,
            energy_regulator=reg_sys,
            memory_governor=evol_gov
        )
    except Exception as e:
        print(f"\n[CRITICAL] DCE initialization failed: {e}")
        exit()

    print("\n" + "="*50)
    print(">>> LIVE INTERACTION LOOP START <<<")
    print("="*50)
    print(" (Type 'quit' to exit)")

    while True:
        try:
            user_in = input("\nYOU: ")
            if user_in.lower() in ["quit", "exit"]:
                break

            # The Magic Happens Here
            resp = dce.handle_interaction(user_in)
            print(f"BOT: {resp}")

        except KeyboardInterrupt:
            print("\n[HARNESS] Interrupted by user.")
            break
        except Exception as e:
            print(f"\n[HARNESS] Runtime Error: {e}")

    print("\n>>> SYSTEM SHUTDOWN <<<")
