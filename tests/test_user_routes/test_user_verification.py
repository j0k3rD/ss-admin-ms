from src.utils.email_context import USER_VERIFY_ACCOUNT
from src.utils.hasher import hash


def test_user_account_verification(client, inactive_user, test_session, db):
    token_context = inactive_user.get_context_string(context=USER_VERIFY_ACCOUNT)
    token = hash(token_context)
    data = {"email": inactive_user.email, "token": token}
    response = client.post("/verify-account", json=data)
    assert response.status_code == 200
    activated_user = test_session.get_user_by_email(email=inactive_user.email)
    assert activated_user.is_active is True
    assert activated_user.verified_at is not None


def test_user_invalid_token(client, inactive_user):
    data = {"email": inactive_user.email, "token": "invalid_token"}
    response = client.post("/verify-account", json=data)
    assert response.status_code == 200
    response = client.post("/verify-account", json=data)
    assert response.status_code != 200


def test_user_invalid_token_does_not_work(client, inactive_user, test_session, db):
    data = {"email": inactive_user.email, "token": "invalid_token"}
    response = client.post("/verify-account", json=data)
    assert response.status_code != 200
    activated_user = test_session.get_user_by_email(email=inactive_user.email)
    assert activated_user.is_active is False
    assert activated_user.verified_at is None


def test_user_invalid_email_does_not_work(client, inactive_user, test_session, db):
    token_context = inactive_user.get_context_string(USER_VERIFY_ACCOUNT)
    token = hash(token_context)
    data = {"email": "test@mailtrap.com", "token": token}
    response = client.post("/verify-account", json=data)
    assert response.status_code != 200
    activated_user = test_session.get_user_by_email(email=inactive_user.email)
    assert activated_user.is_active is False
    assert activated_user.verified_at is None
