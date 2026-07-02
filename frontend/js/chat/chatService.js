
export async function sendClientMessage(chatId, text) {
    const token = localStorage.getItem('iAuthToken');

    const payload = {
        chat_id: chatId,
        raw: text
    };

    const response = await fetch("http://127.0.0.1:8000/chat/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error("Error server synchronization on send");
    return await response.json();
}


export async function fetchChatHistory(chatId) {
    const token = localStorage.getItem('iAuthToken');

    const response = await fetch(`http://127.0.0.1:8000/chat/${chatId}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    if (!response.ok) throw new Error("Error fetching live data streams");
    return await response.json();
}