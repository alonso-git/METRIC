export async function sendClientMessage(text) {

    const iMessagePayload = {
        raw_message: text,
        context: "chat_session_active"
    };

    console.log("Sending serialized iMessage to Server:", JSON.stringify(iMessagePayload));

    // Asynchronous simulation of a response under the iAnalysisResult contract
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                message_intent: "Account Statement Query / Financial Claim",
                support_recommendations: "The client has questions about their current balance. Suggest validating transactions from the last 48 hours and offer downloadable account statements."
            });
        }, 1200);
    });
}