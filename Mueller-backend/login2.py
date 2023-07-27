from flask import Flask, request, jsonify
import jwt
import requests
import logging
from flask_cors import CORS

CORS(app)

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename="/Users/ny/Desktop/pythonn/app.log", level=logging.DEBUG)


@app.route("/login", methods=["POST"])
def login():
    kakao_token = request.post("access_token")
    app.logger.info("Received token: %s", kakao_token)

    headers = {
        "Authorization": f"Bearer {kakao_token}",
    }
    response = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers)
    kakao_user = response.json()

    # 사용자 정보를 로그로 출력
    app.logger.info("User Info: %s", kakao_user)

    token = jwt.encode(
        {"email": kakao_user["email"], "gender": kakao_user["gender"]},
        "Kknnyy0819@@!",
        algorithm="HS256",
    )

    return jsonify({"token": token})


if __name__ == "__main__":
    app.run(port=8000)
