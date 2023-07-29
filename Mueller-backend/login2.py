from flask import Flask, request, jsonify
import jwt
import requests
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(filename="/Users/ny/Desktop/pythonn/app.log", level=logging.DEBUG)


@app.route("/login", methods=["POST"])
def login():
    kakao_token = request.json.get("access_token")
    if kakao_token is None:
        return jsonify({"error": "No access token"}), 400

    print("Received token: ", kakao_token)  # Add this line to print the received token

    headers = {
        "Authorization": f"Bearer {kakao_token}",
    }
    response = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Invalid access token"}), 400
    kakao_user = response.json()

    # 사용자 정보를 로그로 출력
    print("User Info: ", kakao_user)  # Add this line to print the user info

    token = jwt.encode(
        {
            "email": kakao_user["kakao_account"]["email"],
            "gender": kakao_user["kakao_account"]["gender"],
        },
        "Kknnyy0819@@!",
        algorithm="HS256",
    )

    return jsonify({"token": token.decode("utf-8")})


if __name__ == "__main__":
    app.run(port=8000)
