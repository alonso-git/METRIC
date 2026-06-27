import { sendClientMessage } from './chatService.js';

const chatFeed = document.getElementById('chatFeed');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const aiIntent = document.getElementById('aiIntent');
const aiRecommendations = document.getElementById('aiRecommendations');

document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('iAuthToken')) {
        window.location.href = 'index.html';
        return;
    }


    document.getElementById('agentName').innerText = `Agent: ${localStorage.getItem('agentName') || 'Mariana Soto'}`;
});

sendBtn.addEventListener('click', handleOutgoing);
messageInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') handleOutgoing(); });

async function handleOutgoing() {
    const text = messageInput.value.trim();
    if (text === '') return;


    renderBubble('Agent', text, 'bg-blue-600 self-end');
    messageInput.value = '';

    const iAnalysisResult = await sendClientMessage(text);


    aiIntent.innerText = iAnalysisResult.message_intent;
    aiRecommendations.innerHTML = `<p class="text-slate-100">${iAnalysisResult.support_recommendations}</p>`;


    setTimeout(() => {

        renderBubble('Client', "Yes, please. Help me review yesterday's balance.", 'bg-slate-800 text-slate-200');
    }, 1000);
}

function renderBubble(sender, text, bgClass) {
    const wrapper = document.createElement('div');
    wrapper.className = `flex flex-col ${sender === 'Agent' ? 'items-end' : 'items-start'}`;
    wrapper.innerHTML = `
        <span class="text-xs text-slate-500 mb-0.5">${sender}</span>
        <div class="max-w-md p-3 rounded-2xl text-sm ${bgClass}">${text}</div>
    `;
    chatFeed.appendChild(wrapper);
    chatFeed.scrollTop = chatFeed.scrollHeight;
}

document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('iAuthToken');
    window.location.href = 'index.html';
});