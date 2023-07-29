document.addEventListener("DOMContentLoaded", function () {
  // Kakao JavaScript SDK의 초기화와 로그인 버튼에 이벤트 핸들러를 설정합니다.
  Kakao.init("8cd9a7b988003d6821148374f32e3cda");

  document
    .getElementById("kakao-login-btn")
    .addEventListener("click", function () {
      Kakao.Auth.login({
        success: function (authObj) {
          // 로그인 성공 시, 백엔드에 토큰을 전송합니다.
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
            .then((response) => response.json())
            .then((data) => {
              // 백엔드에서 받은 JWT를 로컬 저장소에 저장합니다.
              localStorage.setItem("jwt", data.token);
            });
        },
        fail: function (err) {
          console.log(err);
        },
      });
    });
});
