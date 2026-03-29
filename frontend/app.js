/*
let token = "";
let userId = null;

// TOKEN DECODE (safe)
function getUserIdFromToken(token) {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.sub;
    } catch (e) {
        console.error("Invalid token");
        return null;
    }
}

// LOGIN
async function login() {
    try {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const res = await fetch("http://127.0.0.1:8000/users/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.detail || "Login failed");
            return;
        }

        token = data.access_token;
        userId = getUserIdFromToken(token);

        console.log("TOKEN:", token);
        console.log("User ID:", userId);

        alert("Login Successful");

    } catch (error) {
        console.error(error);
        alert("Login error");
    }
}

// CHECK-IN
async function checkIn() {
    try {
        if (!token || !userId) {
            alert("Please login first");
            return;
        }

        const res = await fetch(`http://127.0.0.1:8000/attendance/check-in/${userId}`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();
        alert(data.msg || data.detail);

    } catch (error) {
        console.error(error);
        alert("Check-in failed");
    }
}

// CHECK-OUT
async function checkOut() {
    try {
        if (!token) {
            alert("Please login first");
            return;
        }

        const res = await fetch("http://127.0.0.1:8000/attendance/check-out", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();
        alert(data.msg || data.detail);

    } catch (error) {
        console.error(error);
        alert("Check-out failed");
    }
}

// MY ATTENDANCE
async function getAttendance() {
    try {
        if (!token) {
            alert("Please login first");
            return;
        }

        const res = await fetch("http://127.0.0.1:8000/attendance/my-attendance", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.detail || "Error fetching attendance");
            return;
        }

        const list = document.getElementById("attendanceList");
        list.innerHTML = "";

        data.forEach(item => {
            const li = document.createElement("li");
            li.innerText = `Date: ${item.date} | In: ${item.check_in_time} | Out: ${item.check_out_time} | Status: ${item.status}`;
            list.appendChild(li);
        });

    } catch (error) {
        console.error(error);
        alert("Error fetching attendance");
    }
}

// ALL ATTENDANCE (ADMIN)
async function getAllAttendance() {
    try {
        if (!token) {
            alert("Please login first");
            return;
        }

        const res = await fetch("http://127.0.0.1:8000/attendance/all-attendance", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();

        console.log("STATUS:", res.status);
        console.log("RESPONSE:", data);

        if (!res.ok) {
            alert(data.detail || "Access denied");
            return;
        }

        const list = document.getElementById("attendanceList");
        list.innerHTML = "";

        data.forEach(item => {
            const li = document.createElement("li");
            li.innerText = `User ID: ${item.user_id} | Date: ${item.date} | In: ${item.check_in_time} | Out: ${item.check_out_time} | Status: ${item.status}`;
            list.appendChild(li);
        });

    } catch (error) {
        console.error(error);
        alert("Failed to fetch all attendance");
    }
}

// for hr portal
async function getMonthlyReport() {
    const userId = document.getElementById("userId").value;

    const res = await fetch(`http://127.0.0.1:8000/attendance/report/monthly?user_id=${userId}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await res.json();
    alert(JSON.stringify(data));
} */

let token = localStorage.getItem("token") || "";
let userId = localStorage.getItem("userId") || null;

// TOKEN DECODE
function parseJwt(token) {
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
        console.error("Invalid token");
        return null;
    }
}

// REGISTER 
async function register() {
    try {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        //const role = document.getElementById("role").value;

        const res = await fetch("http://127.0.0.1:8000/users/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password, role })
        });

        const data = await res.json();
        alert(data.msg || data.detail);

    } catch (error) {
        console.error(error);
        alert("Register failed");
    }
}

// LOGIN 
async function login() {
    try {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // 🔥 ADD: basic validation
        if (!username || !password) {
            alert("Please enter username and password");
            return;
        }

        const res = await fetch("http://127.0.0.1:8000/users/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.detail || "Login failed");
            return;
        }

        token = data.access_token;

        const payload = parseJwt(token);
        userId = payload.sub;
        const role = payload.role;

        // ADD: save role also
        localStorage.setItem("role", role);

        // SAVE IN LOCAL STORAGE
        localStorage.setItem("token", token);
        localStorage.setItem("userId", userId);

        //ADD: debug log (helps a lot)
        console.log("Token:", token);
        console.log("User ID:", userId);
        console.log("Role:", role);

        alert("Login Successful");

        // ADD: slight delay (smooth UX)
        setTimeout(() => {

            // ROLE BASED REDIRECT
            if (role === "admin") {
                window.location.href = "admin.html";
            } else if (role === "hr") {
                window.location.href = "hr.html";
            } else {
                window.location.href = "user.html";
            }

        }, 500);

    } catch (error) {
        console.error(error);

        // ADD: better error message
        alert("Server error or backend not running");
    }
}

//LOGOUT 
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("userId");

    // ADD: also remove role
    localStorage.removeItem("role");

    token = "";
    userId = null;

    // ADD: clear entire storage (extra safety)
    localStorage.clear();

    // ADD: optional message
    alert("Logged out successfully");

    // ADD: debug
    console.log("User logged out");

    window.location.href = "index.html";
}

//checkin 
function checkIn() {
    const userId = localStorage.getItem("userId");
    const token = localStorage.getItem("token");

    console.log("User ID:", userId);
    console.log("Token:", token);

    // 🔥 ADD: decode token to get actual userId
    const payload = parseJwt(token);
    const tokenUserId = payload.sub || payload.user_id;

    console.log("Token User ID:", tokenUserId);

    // ADD: fix mismatch automatically
    if (userId != tokenUserId) {
        console.log("Fixing userId mismatch...");
        localStorage.setItem("userId", tokenUserId);
    }

    // ADD: check if userId is undefined/null string
    if (!userId || userId === "undefined" || userId === "null") {
        alert("User ID missing. Please login again.");
        return;
    }

    // ADD: check if token exists
    if (!token) {
        alert("Token missing. Please login again.");
        return;
    }

    // ADD: show loading
    console.log("Sending check-in request...");

    fetch(`http://127.0.0.1:8000/attendance/check-in/${localStorage.getItem("userId")}`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => {
        // ADD: check unauthorized
        if (res.status === 401) {
            alert("Unauthorized. Please login again.");
            return;
        }
        return res.json();
    })
    .then(data => {
        console.log(data);

        // ADD: handle backend error message
        if (data && data.detail) {
            alert(data.detail);
            return;
        }

        alert(data.msg || data.status);
    })
    .catch(err => {
        console.error(err);
        alert("Check-in failed");
    });
}
// MY ATTENDANCE 
async function getAttendance() {
    try {
        if (!token) {
            alert("Please login first");
            return;
        }

        const res = await fetch("http://127.0.0.1:8000/attendance/my-attendance", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.detail || "Error fetching attendance");
            return;
        }

        const list = document.getElementById("attendanceList");
        list.innerHTML = "";

        data.forEach(item => {
            const li = document.createElement("li");
            li.innerText = `Date: ${item.date} | In: ${item.check_in_time} | Out: ${item.check_out_time} | Status: ${item.status}`;
            list.appendChild(li);
        });

    } catch (error) {
        console.error(error);
        alert("Error fetching attendance");
    }
}

// ALL ATTENDANCE (ADMIN + HR) 
async function getAllAttendance() {
    try {
        if (!token) {
            alert("Please login first");
            return;
        }

        const res = await fetch("http://127.0.0.1:8000/attendance/all-attendance", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.detail || "Access denied");
            return;
        }

        const list = document.getElementById("data");
        list.innerHTML = "";

        data.forEach(item => {
            const li = document.createElement("li");
            li.innerText = `User: ${item.user_id} | Date: ${item.date} | In: ${item.check_in} | Out: ${item.check_out} | Status: ${item.status}`;
            list.appendChild(li);
        });

    } catch (error) {
        console.error(error);
        alert("Failed to fetch all attendance");
    }
}

//  MONTHLY REPORT (HR + ADMIN) 
async function getMonthlyReport() {
    try {
        if (!token) {
            alert("Please login first");
            return;
        }
        const userIdInput = document.getElementById("userId").value;
        const res = await fetch(`http://127.0.0.1:8000/attendance/report/monthly?user_id=${userIdInput}`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });
        const data = await res.json();
        if (!res.ok) {
            alert(data.detail || "Access denied");
            return;
        }
        alert(`
User ID: ${data.user_id}
Month: ${data.month}
Present: ${data.total_present}
Absent: ${data.total_absent}
Late: ${data.late_days}
        `);

    } catch (error) {
        console.error(error);
        alert("Failed to fetch report");
    }
}
//Register funtion 
async function register() {
    try {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        //const role = document.getElementById("role").value;
        if (!username || !password) {
            document.getElementById("msg").innerText = "Please fill all fields";
            return;
        }
        const res = await fetch("http://127.0.0.1:8000/users/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                password,
                //role
            })
        });

        const data = await res.json();
        if (res.ok) {
            document.getElementById("msg").innerText = "Registered Successfully";
            setTimeout(() => {
                window.location.href = "login.html";
            }, 1000);

        } else {
            document.getElementById("msg").innerText = data.detail || "Registration failed";
        }

    } catch (error) {
        console.error(error);
        document.getElementById("msg").innerText = "Something went wrong";
    }
}

// CHECK-OUT
async function checkOut() {
    try {
        if (!token) {
            alert("Please login first");
            return;
        }

        const res = await fetch("http://127.0.0.1:8000/attendance/check-out", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();
        alert(data.msg || data.detail);

    } catch (error) {
        console.error(error);
        alert("Check-out failed");
    }
}

// MY ATTENDANCE
async function getAttendance() {
    try {
        if (!token) {
            alert("Please login first");
            return;
        }

        const res = await fetch("http://127.0.0.1:8000/attendance/my-attendance", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.detail || "Error fetching attendance");
            return;
        }

        const list = document.getElementById("data");
        list.innerHTML = "";

        data.forEach(item => {
            const li = document.createElement("li");
            li.innerText = `Date: ${item.date} | In: ${item.check_in_time} | Out: ${item.check_out_time} | Status: ${item.status}`;
            list.appendChild(li);
        });

    } catch (error) {
        console.error(error);
        alert("Error fetching attendance");
    }
}
