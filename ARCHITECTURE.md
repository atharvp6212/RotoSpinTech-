# Architecture and research design

The Django models support the operational application. Pure functions in
`inventory/research_algorithms.py` support reproducible experiments without
database noise: DAG validation, multi-level BOM explosion, EOQ, reorder points
and capacity-constrained minimum-cost procurement.

The BOM algorithm validates the graph through topological sorting and then
propagates demand once across every edge: `O(V+E)` time and space. The supplier
baseline assumes divisible, independent offers and sorts them by unit price.
It is not suitable when discounts, fixed charges or coupled constraints exist;
those variants require linear or mixed-integer optimization.
