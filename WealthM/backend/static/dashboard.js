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
    

    document.querySelector(".card:nth-child(1) p").innerText = `$${user.net_worth}`;
    document.querySelector(".card:nth-child(3) p").innerText = `$${user.total_assets}`;
    document.querySelector(".card:nth-child(2) p").innerText = `$${user.total_debt}`;
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