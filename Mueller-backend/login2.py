from flask import Flask, request, jsonify
import jwt
import requests

app = Flask(__name__)


@app.route("/login", methods=["POST"])
def login():
    kakao_token = request.json.get("access_token")

    # 카카오 토큰을 카카오에 검증 요청
    headers = {
        "Authorization": f"Bearer {kakao_token}",
    }
    response = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
    kakao_user = response.json()
    # 여기에서 데이터베이스에 사용자를 저장하거나 업데이트하면 됩니다.

    # 사용자 정보로 JWT 생성
    token = jwt.encode(
        {"email": kakao_user["email"], "gender": kakao_user["gender"]},
        "Kknnyy0819@@!",
        algorithm="HS256",
    )

    return jsonify({"token": token})


if __name__ == "__main__":
    login2.run(port=5502)
