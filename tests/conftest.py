import json

import pytest

from iam_sarif_report.adapters import checks
from iam_sarif_report.domain import converter


@pytest.fixture(name="sarif_schema")
def _sarif_schema(shared_datadir):
    schema_path = shared_datadir / "sarif-schema-2.1.0.json"
    yield json.loads(schema_path.read_text())


@pytest.fixture(name="checks_repository")
def _checks_repository():
    yield checks.ChecksPackageDataRepository()


@pytest.fixture(name="sarif_converter")
def _sarif_converter(checks_repository):
    yield converter.SarifConverter(checks_repository=checks_repository)
