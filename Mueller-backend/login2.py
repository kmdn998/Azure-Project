from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
import requests
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 데이터베이스 설정
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://root:Kknnyy0819@@!@localhost/Azure_db"
db = SQLAlchemy(app)


# User 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)


# 사용자 정보를 데이터베이스에 저장
def create_user(email, gender):
    user = User(email=email, gender=gender)
    db.session.add(user)
    db.session.commit()


@app.route("/login", methods=["POST"])
def login():
    kakao_token = request.json.get("access_token")
    if kakao_token is None:
        return jsonify({"error": "No access token"}), 400

    headers = {
        "Authorization": f"Bearer {kakao_token}",
    }
    response = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Invalid access token"}), 400
    kakao_user = response.json()

    token = jwt.encode(
        {
            "email": kakao_user["kakao_account"]["email"],
            "gender": kakao_user["kakao_account"]["gender"],
        },
        "Kknnyy0819@@!",
        algorithm="HS256",
    )

    # 사용자 정보를 데이터베이스에 저장
    create_user(
        kakao_user["kakao_account"]["email"], kakao_user["kakao_account"]["gender"]
    )

    return jsonify({"token": token})


if __name__ == "__main__":
    db.create_all()  # 데이터베이스 테이블 생성
    app.run(port=8000)
