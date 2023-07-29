document.addEventListener("DOMContentLoaded", function () {
  // Kakao JavaScript SDK의 초기화와 로그인 버튼에 이벤트 핸들러를 설정합니다.
  Kakao.init("8cd9a7b988003d6821148374f32e3cda");

  document
    .getElementById("kakao-login-btn")
    .addEventListener("click", function (event) {
      event.preventDefault(); // 추가된 코드
      console.log("Login button clicked");

      Kakao.Auth.login({
        success: function (authObj) {
          // 로그인 성공 시, 백엔드에 토큰을 전송합니다.
          console.log("Login successful");
          console.log(authObj);
          fetch("http://localhost:8000/login", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              access_token: authObj.access_token,
            }),
          })
            .then((response) => {
              if (!response.ok) {
                throw new Error(`POST request failed: ${response.status}`);
              }
              return response.json();
            })
            .then((data) => {
              // 백엔드에서 받은 JWT를 로컬 저장소에 저장합니다.
              localStorage.setItem("jwt", data.token);
            })
            .catch((error) => {
              console.error("Error:", error);
            });
        },
        fail: function (err) {
          console.log(err);
        },
      });
    });
});
