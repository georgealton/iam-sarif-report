from pathlib import Path


def test_url_reader(request, url_reader):
    base_path = Path("tests/data") / "policy_checks"
    policy_path = base_path / "policies" / f"arn-region-not-allowed.json"
    uri = policy_path.absolute().as_uri()
    policy = url_reader(uri)

    assert type(policy) is str
