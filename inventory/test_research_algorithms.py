from django.test import SimpleTestCase

from .research_algorithms import (
    BomCycleError, cheapest_procurement, economic_order_quantity, explode_bom,
    reorder_point,
)


class ResearchAlgorithmTests(SimpleTestCase):
    def test_multilevel_bom_aggregates_shared_material(self):
        edges = [('bike', 'wheel', 2), ('bike', 'frame', 1), ('wheel', 'steel', 3), ('frame', 'steel', 5)]
        self.assertEqual(explode_bom('bike', 2, edges), {'steel': 22})

    def test_cycle_is_rejected(self):
        with self.assertRaises(BomCycleError):
            explode_bom('a', 1, [('a', 'b', 1), ('b', 'a', 1)])

    def test_inventory_formulae(self):
        self.assertAlmostEqual(economic_order_quantity(1000, 20, 5), 89.4427, places=3)
        self.assertEqual(reorder_point(10, 4, 15), 55)

    def test_minimum_cost_procurement(self):
        plan, total = cheapest_procurement({'steel': 8}, [('steel', 'B', 3, 10), ('steel', 'A', 2, 5)])
        self.assertEqual(total, 19)
        self.assertEqual([row[1] for row in plan], ['A', 'B'])
