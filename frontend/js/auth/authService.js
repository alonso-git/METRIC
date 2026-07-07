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