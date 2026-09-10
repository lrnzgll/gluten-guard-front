import time
import random
from typing import TypedDict, Any


class ApiResult(TypedDict):
    risk_score: int
    text: str


MOCK_PRESETS = [
    {
        "risk_score": 88,
        "text": """### Identified Dish: **Classic Pasta Carbonara** 🍝

**Risk Analysis:** High probability of gluten. Traditional Carbonara uses wheat-based semolina pasta (spaghetti/rigatoni) and may occasionally use flour to thicken egg mixture in non-standard recipes.

---

#### 📋 Questions to ask your server:
1. **"Do you offer gluten-free pasta options?"**
2. **"Is gluten-free pasta boiled in a dedicated pot with fresh, uncontaminated water?"**
3. **"Is the guanciale/pancetta seasoned with any soy sauce or flour-based coatings?"**
4. **"Are the cheese and egg prepared on clean surfaces free of flour dust?"**"""
    },
    {
        "risk_score": 95,
        "text": """### Identified Dish: **Neapolitan Margherita Pizza** 🍕

**Risk Analysis:** Very High gluten risk. Standard Neapolitan pizza dough is made from high-gluten wheat flour (Tipo 00). Airborne flour in pizza kitchens also presents cross-contamination risks.

---

#### 📋 Questions to ask your server:
1. **"Do you have a certified gluten-free pizza crust prepared separately?"**
2. **"Is the gluten-free crust baked in a dedicated oven or on a separate clean pan?"**
3. **"Do you use separate pizza cutters and utensils for gluten-free orders?"**
4. **"Is airborne flour present in the prep area where toppings are added?"**"""
    },
    {
        "risk_score": 12,
        "text": """### Identified Dish: **Grilled Salmon with Roasted Vegetables & Quinoa** 🐟🥗

**Risk Analysis:** Low gluten risk. Fresh salmon, vegetables, and olive oil are naturally gluten-free. Quinoa is a gluten-free pseudo-grain.

---

#### 📋 Questions to ask your server:
1. **"Is the salmon prepared on a shared grill surface where breaded items or flour patties are cooked?"**
2. **"Are any soy sauces, teriyaki glazes, or flour-thickened marinades used on the fish or vegetables?"**
3. **"Can the chef use clean foil or a dedicated pan to cook my portion?"**"""
    },
    {
        "risk_score": 35,
        "text": """### Identified Dish: **Crispy Chicken Caesar Salad** 🥗

**Risk Analysis:** Moderate risk. While salad greens and chicken are naturally gluten-free, croutons contain wheat, and commercial Caesar dressings often contain Worcestershire sauce, malt vinegar, or wheat-derived thickeners.

---

#### 📋 Questions to ask your server:
1. **"Can I get this salad strictly WITHOUT croutons, prepared in a fresh mixing bowl?"**
2. **"Is the chicken grilled plain, or is it breaded/marinated with wheat-containing seasonings?"**
3. **"Does your Caesar dressing contain soy sauce, malt vinegar, or flour thickeners?"**"""
    },
]


def call_gluten_guard_api(image_input: Any = None) -> ApiResult:
    """
    Mock API simulating CNN inference + Gluten Risk Engine.
    Returns exactly 2 fields:
      - risk_score (int): percentage value (0-100)
      - text (str): formatted markdown text containing dish identification,
                    risk explanation, and specific restaurant questions.
    """
    # Simulate realistic network / AI inference latency
    time.sleep(1.2)
    
    # Pick a preset deterministically if image has name, or randomly
    if hasattr(image_input, "name") and image_input.name:
        name_lower = image_input.name.lower()
        if "pizza" in name_lower:
            return MOCK_PRESETS[1]
        elif "salmon" in name_lower or "fish" in name_lower or "salad" in name_lower:
            return MOCK_PRESETS[2]
        elif "chicken" in name_lower:
            return MOCK_PRESETS[3]
        
    return random.choice(MOCK_PRESETS)
