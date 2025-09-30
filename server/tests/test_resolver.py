import json


def test_ping_allows_anonymous(client):
    resp = client.get("/api/v1/ping/")
    assert resp.status_code == 200
    data = json.loads(resp.content)
    assert data["status"] == "ok"


def test_default_protection(client):
    # Hitting a non-existent endpoint under api should return 404, but auth middleware is present.
    resp = client.get("/api/v1/protected-example/")
    # Either 401/403/404 depending on routing; just assert not 500
    assert resp.status_code in (401, 403, 404)


def test_db_backed_resolution(client, django_user_model):
    # Create sample data without migrations by using ORM; SQLite ok for tests.
    from apps.authority.models import AuthoritySource, Term, Synonym

    src = AuthoritySource.objects.create(slug="ics-2023", name="ICS", version="2023")
    term = Term.objects.create(source=src, name="Permian", type="period", lang="en")
    Synonym.objects.create(source=src, term=term, name="Perm", lang="en")

    r1 = client.get("/api/v1/resolve/?q=Permian")
    assert r1.status_code == 200
    assert r1.json()["standard_name"] == "Permian"

    r2 = client.get("/api/v1/resolve/?q=Perm")
    assert r2.status_code == 200
    assert r2.json()["standard_name"] == "Permian"
