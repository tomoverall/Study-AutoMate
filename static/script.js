document.getElementById("file").addEventListener("change", function() {
    var fileInput = document.getElementById("file");
    var generateBtn = document.getElementById("generate-btn");

    if (fileInput.files.length > 0) {
        generateBtn.disabled = false;
    } else {
        generateBtn.disabled = true;
    }
});
