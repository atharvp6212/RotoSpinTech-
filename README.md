# Multi-Level Inventory and Material Requirement Optimization System

A Django application for modelling products, sub-parts and the raw materials
required to manufacture them. The project originated from an inventory problem
at Rotospin-Tech and is being developed as a testbed for material-requirement
algorithms, query optimization and performance analysis.

## Current capabilities

- Role-based administrator and worker accounts
- Product, sub-part, colour and raw-material management
- Bill-of-materials relationships with fractional quantities
- Linear-time material aggregation across a product's sub-parts
- Stock-versus-requirement planning with shortage calculation
- Automated tests for aggregation, scaling and validation
- Multi-level DAG expansion with cycle detection
- EOQ, safety-stock reorder points and minimum-cost supplier allocation
- Deterministic time-and-memory benchmark tooling

## Algorithm

For a product with `m` bill-of-material edges, the material planner performs a
single filtered query and one pass over the result. Its aggregation cost is
`O(m)` time and `O(r)` auxiliary space, where `r` is the number of distinct raw
materials. Future work will compare this baseline with recursive CTEs and cached
plans for multi-level bills of materials.

Run `python benchmarks/bom_benchmark.py --depths 10 100 1000` for a
reproducible scalability experiment. See `ARCHITECTURE.md` and `LIMITATIONS.md`
for assumptions that must accompany any reported result.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

Do not use the development settings or SQLite database in production.
