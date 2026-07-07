let tokenPromise = null;

async function getToken() {
    const token = localStorage.getItem('iAuthToken');
    if (token) return token;

    const email = localStorage.getItem('userEmail');
    const password = localStorage.getItem('userPassword');
    if (!email || !password) return null;

    if (!tokenPromise) {
        tokenPromise = fetch("http://127.0.0.1:8000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        }).then(r => {
            tokenPromise = null;
            if (!r.ok) return null;
            return r.json();
        }).then(data => {
            if (!data) return null;
            localStorage.setItem('iAuthToken', data.access_token);
            if (data.user.client_chats && data.user.client_chats.length > 0) {
                localStorage.setItem('client_chat', JSON.stringify(data.user.client_chats[0]));
            }
            if (data.user.agent_chats && data.user.agent_chats.length > 0) {
                localStorage.setItem('agent_chat', JSON.stringify(data.user.agent_chats[0]));
            }
            return data.access_token;
        }).catch(() => {
            tokenPromise = null;
            return null;
        });
    }
    return tokenPromise;
}

export function getChatIdForRole() {
    const role = localStorage.getItem('userRole');
    const key = role === 'agent' ? 'agent_chat' : 'client_chat';
    const stored = localStorage.getItem(key);
    if (!stored) return null;
    try {
        const chat = JSON.parse(stored);
        return (chat && chat.id) ? chat.id : null;
    } catch (e) {
        localStorage.removeItem(key);
        return null;
    }
}

async function apiFetch(url, options) {
    let token = await getToken();
    if (!token) throw new Error("No active session");

    options.headers = options.headers || {};
    options.headers["Authorization"] = `Bearer ${token}`;

    let response = await fetch(url, options);

    if ((response.status === 401 || response.status === 403) && token) {
        localStorage.removeItem('iAuthToken');
        token = await getToken();
        if (!token) throw new Error(`Session expired (${response.status})`);
        options.headers["Authorization"] = `Bearer ${token}`;
        response = await fetch(url, options);
    }

    return response;
}

export async function sendClientMessage(text) {
    const role = localStorage.getItem('userRole');
    let chatId = getChatIdForRole();

    const payload = { raw: text };
    if (chatId) payload.chat_id = chatId;

    console.log("Sending payload:", JSON.stringify(payload));

    let response = await apiFetch("http://127.0.0.1:8000/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (!response.ok && response.status === 404 && chatId) {
        const key = role === 'agent' ? 'agent_chat' : 'client_chat';
        localStorage.removeItem(key);
        chatId = null;
        const retryPayload = { raw: text };
        console.log("Stale chat, retrying without chat_id:", JSON.stringify(retryPayload));
        response = await apiFetch("http://127.0.0.1:8000/chat/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(retryPayload)
        });
    }

    if (!response.ok) {
        throw new Error(`Server error (${response.status})`);
    }

    if (role === 'client' && !chatId) {
        await updateChatsFromLogin();
    }

    return null;
}

async function updateChatsFromLogin() {
    try {
        const response = await fetch("http://127.0.0.1:8000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: localStorage.getItem('userEmail'),
                password: localStorage.getItem('userPassword')
            })
        });
        if (!response.ok) return;
        const data = await response.json();
        if (data.user.client_chats && data.user.client_chats.length > 0) {
            localStorage.setItem('client_chat', JSON.stringify(data.user.client_chats[0]));
        }
        if (data.user.agent_chats && data.user.agent_chats.length > 0) {
            localStorage.setItem('agent_chat', JSON.stringify(data.user.agent_chats[0]));
        }
    } catch (e) {
        console.error("Could not refresh chat list:", e);
    }
}

export async function fetchChatHistory(chatId) {
    if (!chatId) return null;

    const response = await apiFetch(`http://127.0.0.1:8000/chat/${chatId}`, {
        method: "GET"
    });

    if (!response.ok) return null;
    const text = await response.text();
    if (!text) return null;
    return JSON.parse(text);
}