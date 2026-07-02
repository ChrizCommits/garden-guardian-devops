GLOBAL_UNSAFE_FOODS = [
    "milk for hedgehogs",
    "bread for birds",
    "salty, spicy, or cooked leftovers",
    "chocolate",
    "processed human food",
    "honey water for wild bees",
]


def global_safety_warning() -> str:
    foods = ", ".join(GLOBAL_UNSAFE_FOODS)
    return (
        f"Keep support clean and low-risk: avoid {foods}. Do not touch or handle "
        "wild animals unless a qualified rescue service tells you to, and seek "
        "professional help for injured animals."
    )
