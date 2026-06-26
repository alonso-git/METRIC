export async function loginToServer(username, password) {

    return new Promise((resolve) => {
        setTimeout(() => {
            if (username === "mariana" && password === "1234") {
                resolve({
                    status: "success",
                    role: "Support Agent",
                    token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mockTokenForMariana"
                });
            } else {
                resolve({
                    status: "error",
                    message: "incorrect credentials"
                });
            }
        }, 1000);
    });
}