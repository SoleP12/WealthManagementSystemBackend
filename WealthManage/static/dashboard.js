


async function logout(event) {
    localStorage.removeItem("access_token");
    window.location.href = "/";
}