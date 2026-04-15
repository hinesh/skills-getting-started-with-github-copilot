from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_root_redirect():
    # Arrange: No special setup needed

    # Act: Make GET request to root endpoint
    response = client.get("/")

    # Assert: Should serve the static index.html (redirect followed or direct serve)
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text


def test_get_activities():
    # Arrange: No special setup needed

    # Act: Make GET request to activities endpoint
    response = client.get("/activities")

    # Assert: Should return 200 and the activities dictionary
    assert response.status_code == 200
    assert response.json() == activities


def test_signup_for_activity_success():
    # Arrange: Choose an activity and email not already signed up
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Ensure not already signed up
    assert email not in activities[activity_name]["participants"]

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 200 and add the email to participants
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_for_activity_not_found():
    # Arrange: Use a non-existent activity
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 404
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_for_activity_already_signed_up():
    # Arrange: First sign up a student
    activity_name = "Programming Class"
    email = "duplicate@mergington.edu"

    # Sign up first time
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act: Try to sign up again
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 400
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_from_activity_success():
    # Arrange: First sign up a student
    activity_name = "Gym Class"
    email = "unregister@mergington.edu"

    # Sign up
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act: Unregister
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert: Should return 200 and remove from participants
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}


def test_unregister_from_activity_not_found():
    # Arrange: Use a non-existent activity
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert: Should return 404
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_from_activity_not_signed_up():
    # Arrange: Use an activity where the email is not signed up
    activity_name = "Basketball Team"
    email = "notsignedup@mergington.edu"

    # Act: Try to unregister
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert: Should return 400
    assert response.status_code == 400
    assert response.json() == {"detail": "Student not signed up for this activity"}