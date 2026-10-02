ACTIVITY = "Chess Club"


def test_get_activities_returns_activity_details(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activity = response.json()[ACTIVITY]
    assert activity["description"]
    assert activity["schedule"]
    assert activity["max_participants"] > 0
    assert activity["participants"]


def test_signup_adds_participant(client):
    email = "new-student@mergington.edu"

    response = client.post(f"/activities/{ACTIVITY}/signup", params={"email": email})

    assert response.status_code == 200
    assert email in client.get("/activities").json()[ACTIVITY]["participants"]


def test_signup_rejects_unknown_activity(client):
    response = client.post("/activities/Unknown/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{ACTIVITY}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_delete_unregisters_participant(client):
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{ACTIVITY}/signup", params={"email": email})

    assert response.status_code == 200
    assert email not in client.get("/activities").json()[ACTIVITY]["participants"]


def test_delete_rejects_unknown_activity(client):
    response = client.delete("/activities/Unknown/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_rejects_unregistered_participant(client):
    response = client.delete(
        f"/activities/{ACTIVITY}/signup",
        params={"email": "not-registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"