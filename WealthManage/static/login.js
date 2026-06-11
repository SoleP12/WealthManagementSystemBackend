
async function login(event) {
event.preventDefault();


const email = document.getElementById("email").value;
const password = document.getElementById("password").value;

try {
    const response = await fetch("http://localhost:8000/token", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            username: email,
            password: password
        })
    });

    const data = await response.json();

    if (!response.ok) {
        alert(data.detail || "Login failed");
        return;
    }

    localStorage.setItem("access_token", data.access_token);

    window.location.href = "/dashboard";
} catch (error) {
    console.error(error);
    alert("Unable to connect to server");
}


}
