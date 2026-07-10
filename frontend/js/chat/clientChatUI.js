
import { sendClientMessage, fetchChatHistory, getChatIdForRole, heartbeat } from './chatService.js';

const clientChatStream = document.getElementById('clientChatStream');
const clientMessageInput = document.getElementById('clientMessageInput');
const clientSendBtn = document.getElementById('clientSendBtn');

const myUserId = parseInt(localStorage.getItem('userId'));

document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('iAuthToken')) {
        window.location.href = 'index.html';
        return;
    }
    renderClientChat();
    setInterval(renderClientChat, 1500);
});

clientSendBtn.addEventListener('click', handleClientSend);
clientMessageInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') handleClientSend(); });

async function handleClientSend() {
    const text = clientMessageInput.value.trim();
    if (text === '') return;

    console.log("enviando");

    try {
        clientMessageInput.value = '';
        await sendClientMessage(text);
        await renderClientChat();
    } catch (err) {
        console.error("Error connecting with client pipeline:", err);
    }
}

async function renderClientChat() {
    try {
        const chatId = getChatIdForRole();
        if (!chatId) {
            await heartbeat();
            return;
        }
        const chatData = await fetchChatHistory(chatId);
        if (!chatData) return;

        clientChatStream.innerHTML = '';

        chatData.messages.forEach(msg => {
            const isMe = msg.sender_id === myUserId;
            const wrapper = document.createElement('div');
            wrapper.className = `flex space-x-3 items-start ${isMe ? 'justify-end' : 'justify-start'}`;

            if (isMe) {
                wrapper.innerHTML = `
                    <div class="bg-blue-600 border border-blue-500 rounded-2xl px-4 py-2.5 max-w-[85%] text-sm text-white">
                        ${msg.raw}
                    </div>
                `;
            } else {
                wrapper.innerHTML = `
                    <div class="bg-blue-600/20 text-blue-400 border border-blue-500/30 text-xs font-bold px-2 py-1 rounded-md mt-1">AI/Agent</div>
                    <div class="bg-slate-900 border border-slate-800 rounded-2xl px-4 py-2.5 max-w-[85%] text-sm text-slate-200">
                        ${msg.raw}
                    </div>
                `;
            }
            clientChatStream.appendChild(wrapper);
        });
        clientChatStream.scrollTop = clientChatStream.scrollHeight;
    } catch (e) {
        console.log("Syncing database tables...");
    }
}