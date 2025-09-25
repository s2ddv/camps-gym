function togglePassword() {
    const input = document.getElementById("senha");
    const icon = document.getElementById("toggle-icon");

    if (input.type === "password") {
        input.type = "text";
        icon.src = "/frontend/client/src/images/icons8-visível-48.png";
    } else {
        input.type = "password";
        icon.src = "/frontend/client/src/images/icons8-invisível-48.png";
    }
}