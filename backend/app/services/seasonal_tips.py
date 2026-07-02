from __future__ import annotations

from datetime import date
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.animal import Animal
from app.models.card import AnimalCard
from app.models.tip import DailyTip
from app.services.safety import global_safety_warning


ANIMALS = [
    {
        "name": "Bee",
        "category": "Insect",
        "description": "Bees help pollinate flowers, fruit trees, and many garden plants.",
        "image_url": "/images/bee.svg",
        "safe_support_notes": "Grow pesticide-free flowers and provide shallow water with landing stones.",
        "unsafe_foods": "Avoid honey water and processed sugar mixtures.",
    },
    {
        "name": "Wasp",
        "category": "Insect",
        "description": "Wasps are useful predators and pollinators when given space.",
        "image_url": "/images/wasp.svg",
        "safe_support_notes": "Keep distance, avoid swatting, and leave flowering plants available.",
        "unsafe_foods": "Do not offer sweet drinks or human food scraps.",
    },
    {
        "name": "Hedgehog",
        "category": "Mammal",
        "description": "Hedgehogs travel through gardens at night looking for insects and shelter.",
        "image_url": "/images/hedgehog.svg",
        "safe_support_notes": "Offer fresh water, gaps in fences, and quiet leaf or log shelter.",
        "unsafe_foods": "No milk, bread, chocolate, or cooked leftovers.",
    },
    {
        "name": "Blackbird",
        "category": "Bird",
        "description": "Blackbirds search lawns and shrubs for insects, worms, and berries.",
        "image_url": "/images/blackbird.svg",
        "safe_support_notes": "Provide clean water, berry shrubs, and hygienic feeding areas in winter.",
        "unsafe_foods": "No bread, salty food, chocolate, or spoiled leftovers.",
    },
    {
        "name": "Sparrow",
        "category": "Bird",
        "description": "Sparrows thrive around hedges, seed plants, and safe nesting spaces.",
        "image_url": "/images/sparrow.svg",
        "safe_support_notes": "Keep bird water clean and offer suitable seed mixes in cold periods.",
        "unsafe_foods": "No bread, salty food, chocolate, or processed human food.",
    },
    {
        "name": "Squirrel",
        "category": "Mammal",
        "description": "Squirrels use trees and shrubs for cover, food, and movement routes.",
        "image_url": "/images/squirrel.svg",
        "safe_support_notes": "Support them indirectly with native trees, shrubs, and fresh water.",
        "unsafe_foods": "Avoid processed, salted, spicy, or sugary human foods.",
    },
    {
        "name": "Butterfly",
        "category": "Insect",
        "description": "Butterflies need nectar plants and safe places for caterpillars.",
        "image_url": "/images/butterfly.svg",
        "safe_support_notes": "Grow pesticide-free nectar flowers and leave some wild corners.",
        "unsafe_foods": "Avoid pesticide use and artificial feeding mixtures.",
    },
    {
        "name": "Ladybug",
        "category": "Insect",
        "description": "Ladybugs feed on aphids and help keep garden ecosystems balanced.",
        "image_url": "/images/ladybug.svg",
        "safe_support_notes": "Avoid pesticides and leave stems, leaves, and small shelter spaces.",
        "unsafe_foods": "Do not spray pesticides or offer processed food.",
    },
]


CARDS = [
    ("Bee", "Nectar Neighbor", "A bee can visit hundreds of flowers in one foraging trip.", "Common", 1),
    ("Wasp", "Striped Garden Patrol", "Wasps help control many small garden insects naturally.", "Common", 1),
    ("Hedgehog", "Night Walker", "A hedgehog may roam over a kilometer in one night.", "Rare", 2),
    ("Blackbird", "Dawn Singer", "Blackbirds often sing from high perches at dawn and dusk.", "Common", 1),
    ("Sparrow", "Hedge Chatterer", "Sparrows are social birds that benefit from dense shrubs.", "Common", 1),
    ("Squirrel", "Tree Acrobat", "Squirrels remember many food hiding spots by using landmarks.", "Uncommon", 2),
    ("Butterfly", "Bloom Glider", "Butterflies taste with sensors on their feet.", "Uncommon", 2),
    ("Ladybug", "Tiny Aphid Hunter", "Ladybug larvae can eat many aphids while they grow.", "Common", 1),
]


def _tip(
    title: str,
    description: str,
    season: str,
    action: str,
    warning: str,
    animals: list[str],
    reward: int,
    start: int,
    end: int,
) -> dict[str, object]:
    return {
        "title": title,
        "description": description,
        "month_or_season": season,
        "action_instruction": action,
        "safety_warning": f"{warning} {global_safety_warning()}",
        "supported_animals": animals,
        "points_reward": reward,
        "active_from_month": start,
        "active_to_month": end,
    }


TIPS = [
    _tip(
        "Clean winter bird water",
        "A small clean water dish helps birds when frost or dry weather makes drinking harder.",
        "Winter",
        "Rinse a shallow bird water dish and refill it with fresh water.",
        "If feeding birds, use suitable bird food and keep feeders hygienic. Never give bread.",
        ["Blackbird", "Sparrow"],
        1,
        12,
        2,
    ),
    _tip(
        "First flowers, no pesticides",
        "Early blossoms support insects waking up as the weather warms.",
        "Spring",
        "Protect or plant pesticide-free flowering plants such as herbs or native blooms.",
        "Avoid pesticide sprays and avoid honey water for wild bees.",
        ["Bee", "Butterfly", "Ladybug", "Wasp"],
        1,
        3,
        5,
    ),
    _tip(
        "Safe summer water station",
        "Hot days are easier for garden wildlife when clean water is available safely.",
        "Summer",
        "Place a shallow water bowl outside with stones so insects can land safely.",
        "Refresh water daily to prevent hygiene problems and do not add sugar or honey.",
        ["Bee", "Wasp", "Butterfly", "Blackbird", "Sparrow", "Hedgehog"],
        1,
        6,
        8,
    ),
    _tip(
        "Leave a quiet leaf corner",
        "A small natural corner can become shelter for insects and nighttime visitors.",
        "Autumn",
        "Leave some leaves, twigs, or a log pile in a quiet corner of the garden.",
        "Do not handle wild animals, and never give hedgehogs milk.",
        ["Hedgehog", "Ladybug", "Butterfly"],
        1,
        9,
        11,
    ),
]


def seed_sample_data(session: Session) -> None:
    if session.scalar(select(Animal).limit(1)):
        return

    animals_by_name: dict[str, Animal] = {}
    for item in ANIMALS:
        animal = Animal(**item)
        session.add(animal)
        animals_by_name[animal.name] = animal
    session.flush()

    for animal_name, title, fact, rarity, points_value in CARDS:
        session.add(
            AnimalCard(
                animal_id=animals_by_name[animal_name].id,
                title=title,
                fact=fact,
                rarity=rarity,
                points_value=points_value,
                image_url=animals_by_name[animal_name].image_url,
            )
        )

    for item in TIPS:
        session.add(
            DailyTip(
                title=str(item["title"]),
                description=str(item["description"]),
                month_or_season=str(item["month_or_season"]),
                action_instruction=str(item["action_instruction"]),
                safety_warning=str(item["safety_warning"]),
                supported_animals=json.dumps(item["supported_animals"]),
                points_reward=int(item["points_reward"]),
                active_from_month=int(item["active_from_month"]),
                active_to_month=int(item["active_to_month"]),
            )
        )
    session.commit()


def decode_supported_animals(tip: DailyTip) -> list[str]:
    return list(json.loads(tip.supported_animals))


def tip_matches_month(tip: DailyTip, month: int) -> bool:
    if tip.active_from_month <= tip.active_to_month:
        return tip.active_from_month <= month <= tip.active_to_month
    return month >= tip.active_from_month or month <= tip.active_to_month


def get_tip_for_date(session: Session, today: date | None = None) -> DailyTip:
    today = today or date.today()
    tips = [tip for tip in session.scalars(select(DailyTip)).all() if tip_matches_month(tip, today.month)]
    if not tips:
        tips = session.scalars(select(DailyTip)).all()
    tips.sort(key=lambda tip: tip.id)
    return tips[(today.day - 1) % len(tips)]
