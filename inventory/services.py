"""Material-requirement calculations for inventory planning.

The calculation deliberately lives outside views and models so it can be tested,
profiled and reused by a web view, API or batch job.
"""

from collections import defaultdict
from decimal import Decimal

from .models import Product, RawMaterial, SubPartRawMaterial


def calculate_product_requirements(product: Product, units: int = 1) -> dict[int, Decimal]:
    """Return raw-material quantities required to manufacture ``units`` products.

    Related rows are fetched in one query and aggregated in memory. If ``m`` is
    the number of BOM edges, the aggregation is O(m) time and O(r) space, where
    ``r`` is the number of distinct raw materials.
    """
    if units <= 0:
        raise ValueError("units must be a positive integer")

    requirements: dict[int, Decimal] = defaultdict(Decimal)
    bom_rows = SubPartRawMaterial.objects.filter(
        sub_part__product=product
    ).values_list("raw_material_id", "quantity_required")

    multiplier = Decimal(units)
    for material_id, quantity_required in bom_rows:
        requirements[material_id] += Decimal(str(quantity_required)) * multiplier
    return dict(requirements)


def build_material_plan(product: Product, units: int = 1) -> list[dict]:
    """Return requirements, current stock and shortage for each material."""
    requirements = calculate_product_requirements(product, units)
    materials = RawMaterial.objects.in_bulk(requirements)
    plan = []
    for material_id, required in requirements.items():
        material = materials[material_id]
        available = Decimal(str(material.quantity))
        plan.append({
            "material_id": material_id,
            "name": material.name,
            "required": required,
            "available": available,
            "shortage": max(Decimal("0"), required - available),
        })
    return sorted(plan, key=lambda row: row["name"].casefold())
