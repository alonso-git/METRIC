

export async function loginToServer(username, password) {
    return new Promise((resolve) => {
        setTimeout(() => {
            const userLower = username.toLowerCase();

            if (userLower === "mariana" && password === "1234") {
                resolve({
                    status: "success",
                    token: "eyJhbGci...mockAgentToken",
                    user: {
                        full_name: "Mariana Soto",
                        role: "Support Agent"
                    }
                });
            }

            else if (userLower === "customer" && password === "1234") {
                resolve({
                    status: "success",
                    token: "eyJhbGci...mockCustomerToken",
                    user: {
                        full_name: "Client Account",
                        role: "Customer"
                    }
                });
            } else {
                resolve({ status: "error", message: "Invalid credentials." });
            }
        }, 1000);
    });
}


export async function registerToServer(username, password) {
    return new Promise((resolve) => {
        setTimeout(() => {
            console.log(`Sending plain text credentials to Alonso's backend -> User: ${username}`);
            resolve({
                status: "success",
                message: "Account created successfully! Switching to login..."
            });
        }, 1200);
    });
}