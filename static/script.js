document.getElementById("upload-btn").addEventListener("click", function () {
  let formData = new FormData();
  formData.append("aadhar", document.getElementById("aadhar-file").files[0]);
  formData.append(
    "smartcard",
    document.getElementById("smartcard-file").files[0]
  );

  document.getElementById("verification-overlay").style.display = "flex";

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      setTimeout(() => {
        document.getElementById("verification-overlay").style.display = "none";
      }, 5000000); // ⏳ Increased delay from 2000ms (2 sec) to 5000ms (5 sec)
    })
    .catch((error) => {
      document.getElementById("verification-overlay").style.display = "none";
    });
});
