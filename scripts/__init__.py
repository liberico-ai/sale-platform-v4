"""IBS HI Sale Platform v4 - Import scripts.

One-time scripts for data population during Phase 1 setup:
- import_customers.py: Load ~988 customers from Workflow 2026
- import_pipeline.py: Load ~25 opportunities from IBSHI Potential
- import_khkd.py: Load KHKD 2026-2027 targets
- seed_templates.py: Load 6 email templates
"""

__all__ = [
    "import_customers",
    "import_pipeline",
    "import_khkd",
    "seed_templates",
]
