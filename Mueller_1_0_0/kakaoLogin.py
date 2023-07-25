from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/oauth/kakao/callback', methods=['GET'])
def kakao_callback():
    code = request.args.get('code')  # 인가 코드를 URL 파라미터에서 받아옵니다.
    
    # 이제 이 코드를 이용해 토큰을 얻는 등의 추가 로직을 구현하시면 됩니다.
    # 카카오 토큰 얻기 요청을 보내는 예:
    url = "https://kauth.kakao.com/oauth/authorize?client_id=278707778b749aaa8cd7ff5422152e9c&redirect_uri=http://localhost:5502/oauth/kakao/callback&response_type=code"
    payload = {
        "grant_type": "authorization_code",
        "client_id": "278707778b749aaa8cd7ff5422152e9c",
        "redirect_uri": "http://localhost:5502/oauth/kakao/callback",
        "code": code,
    }
    response = requests.post(url, data=payload)
    token = response.json().get('access_token')  # 토큰을 JSON 응답에서 받아옵니다.
    
    # ...
    
    return "Success!"

if __name__ == "__main__":
    app.run(port=5502)
