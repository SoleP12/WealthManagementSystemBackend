async function loadDashboard() {
    const token = localStorage.getItem("access_token");

    if (!token) {
        window.location.href = "/";
        return;
    }

    const response = await fetch("/api/users/me", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    if (response.status === 401) {
        localStorage.removeItem("access_token");
        window.location.href = "/";
        return;
    }

    const user = await response.json();
    
    document.getElementById("net_worth").innerText =  `$${user.net_worth}`;
    document.getElementById("total_assets").innerText =  `$${user.total_assets}`;
    document.getElementById("total_debt").innerText =  `$${user.total_debt}`;

}

async function logout(event) {
    event.preventDefault();
    localStorage.removeItem("access_token");
    window.location.href = "/";
}

document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();

    document.getElementById("logoutBtn")
        .addEventListener("click", logout);
});