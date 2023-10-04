function previewImages(event) {
  let reader = new FileReader();
  const output = document.getElementById("imagePreview");
  output.innerHTML = ""; // 이미지 미리보기를 초기화합니다.

  for (let i = 0; i < event.target.files.length; i++) {
    reader.onload = function () {
      const img = document.createElement("img");
      img.src = reader.result;
      img.classList.add("img-upload-fit");

      // 미리보기 이미지를 출력합니다.
      output.appendChild(img);
    };
    
    reader.readAsDataURL(event.target.files[i]);
  }
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