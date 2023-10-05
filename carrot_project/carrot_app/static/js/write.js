function previewImage(event) {
  let reader = new FileReader();
  reader.onload = function () {
    let output = document.getElementById("imagePreview");
    output.src = reader.result;
    output.classList.add("img-upload-fit");
  };
  reader.readAsDataURL(event.target.files[0]);
}



document.addEventListener("DOMContentLoaded", function() {
  // 가격 필드 요소를 가져옵니다.
  const priceField = document.querySelector("input[name='price']");
  console.log(priceField);

  // 두 번째 form 요소를 선택합니다.
  const secondForm = document.querySelectorAll("form")[1];

  // 폼 제출 이벤트를 감지하고 가격 필드의 값이 숫자가 아닌 경우 경고 메시지를 표시합니다.
  secondForm.addEventListener("submit", function(event) {
    const priceValue = parseFloat(priceField.value);
    console.log(priceValue);
    if (isNaN(priceValue) || priceValue <= 0) {
      event.preventDefault(); // 폼 제출을 중지합니다.
      alert("가격에 숫자만 입력해주세요.");
    }
  });
  const imageField = document.querySelector("input[name='images']");

  // 이미지 필드의 값이 비어있을 때 알람을 표시합니다.
  secondForm.addEventListener("submit", function(event) {
    if (imageField.files.length === 0) {
      event.preventDefault(); // 폼 제출을 중지합니다.
      alert("사진을 선택해주세요.");
    }
  });
});