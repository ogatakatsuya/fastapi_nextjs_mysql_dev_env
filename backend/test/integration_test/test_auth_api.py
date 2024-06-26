from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_register_new_account_ResisterUser_ReturnSuccessMessage():
    response = client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    assert response.status_code == 200
    assert response.json() == {"message": "user created."}

def test_login_for_access_token_LoginWithValidCredentials_ReturnsAccessToken():
    # まずユーザーを登録
    client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
    # ログインを試みる
    response = client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    assert "access_token" in response.cookies

# def test_login_for_access_token_LoginWithInvalidCredentials_ReturnsUnauthorized():
#     # ログインを試みる
#     response = client.post("/auth/login", data={"username": "test_user", "password": "wrong_password"})
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Incorrect username or password"}

# def test_logout_user_LogoutUser_RemovesAccessToken():
#     # まずユーザーを登録してログイン
#     client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
#     client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
#     # ログアウトを試みる
#     response = client.delete("/auth/logout")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Successfully log out"}
#     # クッキーが削除されているか確認
#     assert "access_token" not in response.cookies

# def test_get_user_id_GetUserIdWithValidToken_ReturnsUserId():
#     # まずユーザーを登録してログイン
#     client.post("/auth/register", json={"user_name": "test_user", "password": "test_password"})
#     login_response = client.post("/auth/login", data={"username": "test_user", "password": "test_password"})
#     access_token = login_response.cookies.get("access_token")
#     # ユーザーIDを取得
#     response = client.get("/user", cookies={"access_token": access_token})
#     assert response.status_code == 200
#     assert response.json() == 1  # 登録したユーザーのIDが1と仮定

# def test_get_user_id_GetUserIdWithInvalidToken_ReturnsUnauthorized():
#     # ユーザーIDを取得（無効なトークン）
#     response = client.get("/user", cookies={"access_token": "invalid_token"})
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Not authenticated"}
