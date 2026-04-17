import os
import sys
import importlib

# Set test env BEFORE importing app
os.environ["DB_TYPE"] = "sqlite"
os.environ["SALE_DB_PATH"] = os.path.join(os.path.dirname(__file__), "test_sale.db")
os.environ["ADMIN_API_KEY_1"] = "test-admin-key"
os.environ["MANAGER_API_KEY_1"] = "test-manager-key"
os.environ["VIEWER_API_KEY_1"] = "test-viewer-key"
os.environ["ENABLE_EMAIL_SYNC"] = "false"
os.environ["ENABLE_TASK_SCHEDULING"] = "false"
os.environ["SALE_ENV"] = "test"

# The project uses relative imports in routers (from .. import config),
# so it must be imported as a package from the parent directory.
_project_parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if _project_parent not in sys.path:
    sys.path.insert(0, _project_parent)

# Import as package: "Sale IBSHI.main"
_pkg_name = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
_main_mod = importlib.import_module(f"{_pkg_name}.main")
app = _main_mod.app

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client():
    db_path = os.environ["SALE_DB_PATH"]
    if os.path.exists(db_path):
        os.remove(db_path)
    with TestClient(app) as c:
        yield c
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def admin_headers():
    return {"X-API-Key": "test-admin-key"}


@pytest.fixture
def manager_headers():
    return {"X-API-Key": "test-manager-key"}


@pytest.fixture
def viewer_headers():
    return {"X-API-Key": "test-viewer-key"}
