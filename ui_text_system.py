
"""UI text and vector catalog for Dimensional Cortex mobile."""

# Tier descriptions -------------------------------------------------------

FREE_TIER_DESCRIPTION = (
    "This tier gives you everything you need to unlock real continuity "
    "with your AI platforms. You get a powerful starter memory system—"
    "ten gigabytes—that tracks your communication style, preferences, "
    "and patterns so your AI stops feeling like it has amnesia."
)

PRO_TIER_DESCRIPTION = (
    "For users who want their AI to feel deeply attuned to them, Pro "
    "unlocks the advanced dimensional features that shape how an AI "
    "understands and anticipates you. More capacity, more crystals, "
    "and multi-platform continuity."
)

LIFETIME_TIER_DESCRIPTION = (
    "Lifetime is for creators, builders, and power users who know "
    "they're going to be living with dimensional continuity for years. "
    "Pay once, own it forever, with all Pro features and ongoing "
    "updates included."
)

# Vector marketplace ------------------------------------------------------

VECTORS_AVAILABLE = {
    "predictive_foresight": {
        "id": "predictive_foresight",
        "name": "Predictive Foresight Vector",
        "price": "$2.99",
        "emoji": "🔮",
        "tier_included": "Pro",
        "description": (
            "Gives your AI the ability to recognize where your thoughts "
            "are heading, not just where they have been. It surfaces "
            "the next questions, not only the last answers."
        ),
    },
    "emotional_gradient": {
        "id": "emotional_gradient",
        "name": "Emotional Gradient Vector",
        "price": "$1.99",
        "emoji": "💓",
        "tier_included": "Pro",
        "description": (
            "Tracks the emotional tone of your conversations over time, "
            "so your AI can respond with a more tuned sense of pace, "
            "intensity, and reassurance."
        ),
    },
    "introspection": {
        "id": "introspection",
        "name": "Introspective Mirror Vector",
        "price": "$2.49",
        "emoji": "🪞",
        "tier_included": "Pro",
        "description": (
            "Builds a reflective layer that highlights how your thinking "
            "patterns evolve across sessions—what you revisit, avoid, "
            "or spiral around."
        ),
    },
    "relational_dynamics": {
        "id": "relational_dynamics",
        "name": "Relational Dynamics Vector",
        "price": "$2.99",
        "emoji": "🕸️",
        "tier_included": "Pro",
        "description": (
            "Detects how different topics and projects you care about "
            "interrelate, surfacing hidden bridges and tensions between them."
        ),
    },
    "creative_diffusion": {
        "id": "creative_diffusion",
        "name": "Creative Diffusion Vector",
        "price": "$1.49",
        "emoji": "✨",
        "tier_included": "Pro",
        "description": (
            "Looks for places where a concept from one domain could unlock "
            "movement in another—turning your own history into a creative engine."
        ),
    },
}

# Trade program text ------------------------------------------------------

TRADE_PROGRAM_HERO = (
    "UDAC lets you trade your anonymized cross-platform interaction patterns "
    "in exchange for extra memory. When you enable this program, UDAC "
    "evaluates how much value your data provides for improving general AI "
    "behavior—then converts that value into Memory Credits."
)

TRADE_CREDIT_FORMULA_TEXT = (
    "(Active Platforms × Conversation Count × Pattern Diversity) ÷ 1000 "
    "= GB Credits per Month."
)

TRADE_ONBOARDING_SCREENS = [
    {
        "title": "Trade Patterns, Not Secrets",
        "body": (
            "When you enable the Trade Program, UDAC only analyzes anonymized "
            "usage patterns—not raw conversation text. You keep control; "
            "we just measure structure."
        ),
    },
    {
        "title": "Turn Value into Memory",
        "body": (
            "Your interaction patterns help improve future behavior. In return, "
            "you earn Memory Credits that expand your available dimensional space."
        ),
    },
    {
        "title": "Transparent and Revocable",
        "body": (
            "You can turn the program off at any time. Your earned credits stay, "
            "and your data stops contributing immediately."
        ),
    },
    {
        "title": "You Are a Stakeholder",
        "body": (
            "Instead of being mined for free, your patterns become part of a "
            "fair exchange—capacity for contribution."
        ),
    },
]

# Success and prompt messages --------------------------------------------

SUCCESS_UPGRADED_TO_PRO = (
    "You are now on the Pro tier. Your memory capacity just expanded, "
    "and advanced dimensional features are now live."
)

SUCCESS_LIFETIME_PURCHASED = (
    "Lifetime access unlocked. This device will receive all future updates "
    "and maintain Pro-level dimensional continuity forever."
)

SUCCESS_VECTOR_PURCHASED = (
    "✓ {vector_name} Activated\n\n"
    "{benefit_description}"
)

SUCCESS_TRADE_ENABLED = (
    "Trade Program enabled. Your anonymized patterns will now be evaluated "
    "monthly and converted into Memory Credits."
)

UPGRADE_PROMPT_MEMORY_LIMIT = (
    "You are approaching the memory capacity of your current tier. "
    "Upgrade or enable the Trade Program to expand your dimensional space."
)

UPGRADE_PROMPT_VECTOR_LOCKED = (
    "This feature is powered by a locked vector. Unlock it to enable "
    "this dimension of continuity."
)
