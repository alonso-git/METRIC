/
export async function loginToServer(username, password) {

    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData
    });

    if (!response.ok) {
        throw new Error("Credenciales inválidas. Inténtalo de nuevo.");
    }

    const data = await response.json();

    const profileResponse = await fetch("http://127.0.0.1:8000/auth/my-profile", {
        method: "GET",
        headers: { "Authorization": `Bearer ${data.access_token}` }
    });

    if (!profileResponse.ok) {
        throw new Error("Error al recuperar el perfil del usuario.");
    }

    const profileData = await profileResponse.json();

    return {
        token: data.access_token,
        role: profileData.role,
        name: profileData.name,
        user_id: profileData.id
    };
}