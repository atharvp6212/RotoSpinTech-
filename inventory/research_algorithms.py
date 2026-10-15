"""Pure algorithms for multi-level material and procurement experiments."""

from collections import defaultdict, deque
from dataclasses import dataclass
from math import sqrt


class BomCycleError(ValueError):
    pass


def explode_bom(root: str, quantity: float, edges: list[tuple[str, str, float]]) -> dict[str, float]:
    """Expand a multi-level BOM in O(V+E) after topological validation."""
    if quantity <= 0 or any(multiplier <= 0 for _, _, multiplier in edges):
        raise ValueError('Quantities must be positive.')
    children = defaultdict(list)
    indegree = defaultdict(int)
    nodes = {root}
    for parent, child, multiplier in edges:
        children[parent].append((child, multiplier))
        indegree[child] += 1
        nodes.update((parent, child))
    queue = deque(sorted(node for node in nodes if indegree[node] == 0))
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for child, _ in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(nodes):
        raise BomCycleError('The bill of materials contains a cycle.')
    demand = defaultdict(float, {root: quantity})
    for node in order:
        for child, multiplier in children[node]:
            demand[child] += demand[node] * multiplier
    component_nodes = {parent for parent, _, _ in edges}
    return {node: value for node, value in demand.items() if node not in component_nodes}


def economic_order_quantity(annual_demand: float, ordering_cost: float, annual_holding_cost: float) -> float:
    if min(annual_demand, ordering_cost, annual_holding_cost) <= 0:
        raise ValueError('EOQ inputs must be positive.')
    return sqrt(2 * annual_demand * ordering_cost / annual_holding_cost)


def reorder_point(daily_demand: float, lead_time_days: float, safety_stock: float = 0) -> float:
    if min(daily_demand, lead_time_days, safety_stock) < 0:
        raise ValueError('Reorder-point inputs cannot be negative.')
    return daily_demand * lead_time_days + safety_stock


def cheapest_procurement(requirements: dict[str, float], offers: list[tuple[str, str, float, float]]):
    """Greedily fill divisible supplier offers at minimum cost per material."""
    by_material = defaultdict(list)
    for material, supplier, unit_cost, capacity in offers:
        if unit_cost < 0 or capacity < 0:
            raise ValueError('Offer cost and capacity cannot be negative.')
        by_material[material].append((unit_cost, supplier, capacity))
    plan, total = [], 0.0
    for material, required in sorted(requirements.items()):
        remaining = required
        for cost, supplier, capacity in sorted(by_material[material]):
            purchased = min(remaining, capacity)
            if purchased:
                plan.append((material, supplier, purchased, purchased * cost))
                total += purchased * cost
                remaining -= purchased
            if remaining <= 1e-9:
                break
        if remaining > 1e-9:
            raise ValueError(f'Insufficient supplier capacity for {material}.')
    return plan, total
