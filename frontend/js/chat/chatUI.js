
import { sendClientMessage, fetchChatHistory } from './chatService.js';

const chatFeed = document.getElementById('chatFeed');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const aiIntent = document.getElementById('aiIntent');
const aiRecommendations = document.getElementById('aiRecommendations');


let currentChatId = 1;
const myUserId = parseInt(localStorage.getItem('userId'));

document.addEventListener('DOMContentLoaded', () => {

    if (!localStorage.getItem('iAuthToken')) {
        window.location.href = 'index.html';
        return;
    }

    document.getElementById('agentName').innerText = `Agent: ${localStorage.getItem('agentName') || 'Mariana Soto'}`;


    renderLiveChat();
    setInterval(renderLiveChat, 1500);
});

sendBtn.addEventListener('click', handleOutgoing);
messageInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') handleOutgoing(); });

async function handleOutgoing() {
    const text = messageInput.value.trim();
    if (text === '') return;

    try {
        messageInput.value = '';

        await sendClientMessage(currentChatId, text);

        await renderLiveChat();
    } catch (err) {
        console.error("Failed to route message:", err);
    }
}

async function renderLiveChat() {
    try {
        const chatData = await fetchChatHistory(currentChatId);


        chatFeed.innerHTML = '<div class="text-center text-slate-500 text-xs my-2">Chat started securely. Local link active</div>';


        chatData.messages.forEach(msg => {
            if (msg.sender_id === myUserId) {
                renderBubble('Agent', msg.raw, 'bg-blue-600 self-end text-white');
            } else {
                renderBubble('Client', msg.raw, 'bg-slate-800 text-slate-200 self-start');
            }
        });


        aiIntent.innerText = chatData.overall_intent || "Analyzing intent...";
        aiRecommendations.innerHTML = `<p class="text-slate-100">${chatData.recommendations || 'Waiting for insights...'}</p>`;

    } catch (error) {
        console.log("Polling database stream, waiting for agent assignment sync...");
    }
}

function renderBubble(sender, text, bgClass) {
    const wrapper = document.createElement('div');
    const isAgent = sender === 'Agent';
    wrapper.className = `flex flex-col ${isAgent ? 'items-end' : 'items-start'}`;
    wrapper.innerHTML = `
        <span class="text-xs text-slate-500 mb-0.5">${sender}</span>
        <div class="max-w-md p-3 rounded-2xl text-sm ${bgClass}">${text}</div>
    `;
    chatFeed.appendChild(wrapper);
    chatFeed.scrollTop = chatFeed.scrollHeight;


    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.clear();
        window.location.href = 'index.html';
    });