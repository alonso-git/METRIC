export async function loginToServer(username, password) {
    console.log("Pero si o pura kk?");
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "email": username, "password": password })
    });

    if (!response.ok) {
        throw new Error("Credenciales inválidas. Inténtalo de nuevo.");
    }

    const data = await response.json();

    console.log(data);

    const profileResponse = await fetch("http://127.0.0.1:8000/auth/my-profile", {
        method: "GET",
        headers: { "Authorization": `Bearer ${data.access_token}` }
    });

    if (!profileResponse.ok) {
        throw new Error("Error al recuperar el perfil del usuario.");
    }

    const profileData = await profileResponse.json();

    const result = {
        token: data.access_token,
        role: data.user.role,
        name: data.user.name,
        user_id: data.user.id,
        client_chat: data.user.client_chats[0],
        agent_chat: data.user.agent_chats[0],
        welcomeMessage: profileData.message
    };

    return result;
}

export async function registerClient(name, email, password) {
    const response = await fetch("http://127.0.0.1:8000/users/clients", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    });

    if (!response.ok) {
        const error = await response.text();
        try {
            const jsonError = JSON.parse(error);
            throw new Error(jsonError.detail || "Error al registrar cliente");
        } catch (e) {
            throw new Error(error || "Error al registrar cliente");
        }
    }

    return response.json();
}

export async function registerAgent(name, email, password) {
    const response = await fetch("http://127.0.0.1:8000/users/agents", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    });

    if (!response.ok) {
        const error = await response.text();
        try {
            const jsonError = JSON.parse(error);
            throw new Error(jsonError.detail || "Error al registrar agente");
        } catch (e) {
            throw new Error(error || "Error al registrar agente");
        }
    }

    return response.json();
}