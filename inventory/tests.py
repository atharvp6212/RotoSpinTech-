from decimal import Decimal

from django.test import TestCase

from .models import Product, RawMaterial, SubPart, SubPartRawMaterial
from .services import build_material_plan, calculate_product_requirements


class MaterialPlanningTests(TestCase):
    def setUp(self):
        self.polymer = RawMaterial.objects.create(name="Polymer", quantity=10)
        self.pigment = RawMaterial.objects.create(name="Pigment", quantity=1)
        body = SubPart.objects.create(name="Body")
        lid = SubPart.objects.create(name="Lid")
        self.product = Product.objects.create(name="Container")
        self.product.sub_parts.add(body, lid)
        SubPartRawMaterial.objects.create(
            sub_part=body, raw_material=self.polymer, quantity_required=1.5
        )
        SubPartRawMaterial.objects.create(
            sub_part=lid, raw_material=self.polymer, quantity_required=0.5
        )
        SubPartRawMaterial.objects.create(
            sub_part=body, raw_material=self.pigment, quantity_required=0.25
        )

    def test_requirements_are_aggregated_across_subparts(self):
        result = calculate_product_requirements(self.product, units=4)
        self.assertEqual(result[self.polymer.id], Decimal("8.0"))
        self.assertEqual(result[self.pigment.id], Decimal("1.00"))

    def test_material_plan_reports_shortage(self):
        plan = {row["name"]: row for row in build_material_plan(self.product, units=8)}
        self.assertEqual(plan["Polymer"]["shortage"], Decimal("6.0"))
        self.assertEqual(plan["Pigment"]["shortage"], Decimal("1.00"))

    def test_units_must_be_positive(self):
        with self.assertRaisesMessage(ValueError, "positive"):
            calculate_product_requirements(self.product, units=0)
