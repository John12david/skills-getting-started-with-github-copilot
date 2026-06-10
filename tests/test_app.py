from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert expected_activity in data
    assert "description" in data[expected_activity]
    assert "participants" in data[expected_activity]
    assert data[expected_activity]["participants"] == activities[expected_activity]["participants"]


def test_signup_for_activity_adds_new_participant():
    # Arrange
    activity_name = "Chess Club"
    test_email = "teststudent@mergington.edu"
    assert test_email not in activities[activity_name]["participants"]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email},
    )

    # Assert
    try:
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {test_email} for {activity_name}"
        assert test_email in activities[activity_name]["participants"]
    finally:
        if test_email in activities[activity_name]["participants"]:
            activities[activity_name]["participants"].remove(test_email)


def test_signup_duplicate_returns_400():
    # Arrange
    activity_name = "Programming Class"
    existing_email = activities[activity_name]["participants"][0]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_nonexistent_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Club"
    test_email = "nobody@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
