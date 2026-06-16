def test_root_redirect(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"].startswith("Learn strategies")


def test_signup_for_activity(client):
    activity = "Chess Club"
    email = "test.user@example.com"

    signup_response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for {activity}"

    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_duplicate_signup_returns_400(client):
    email = "michael@mergington.edu"
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_unregister_from_activity(client):
    email = "michael@mergington.edu"
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": email},
    )
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_signup_for_missing_activity_returns_404(client):
    response = client.post(
        "/activities/Nonexistent/signup",
        params={"email": "jane@mergington.edu"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "missing@example.com"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
