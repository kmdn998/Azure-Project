from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
import jwt
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 데이터베이스 설정
password = "Kknnyy0819@@!"
url_encoded_password = quote_plus(password)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://root:{url_encoded_password}@localhost/Azure_db"
db = SQLAlchemy(app)


# User 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)


# 사용자 정보를 데이터베이스에 저장
def create_user(email, gender):
    user = User.query.filter_by(email=email).first()
    if user:
        return "existing_user"

    new_user = User(email=email, gender=gender)
    db.session.add(new_user)
    db.session.commit()
    return "new_user"


@app.route("/login", methods=["POST"])
def login():
    kakao_token = request.json.get("access_token")
    if kakao_token is None:
        return jsonify({"error": "No access token"}), 400

    headers = {"Authorization": f"Bearer {kakao_token}"}
    response = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Invalid access token"}), 400
    kakao_user = response.json()

    email = kakao_user["kakao_account"]["email"]
    gender = kakao_user["kakao_account"]["gender"]

    message = create_user(email, gender)

    token = jwt.encode(
        {"email": email, "gender": gender},
        "Kknnyy0819@@!",
        algorithm="HS256",
    )

    return jsonify({"message": message, "token": token})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=7700)
