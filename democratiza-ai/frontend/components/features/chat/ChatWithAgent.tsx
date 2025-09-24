import React, { useState, useEffect } from 'react';
import { sendMessage } from '../../../lib/api';

const ChatWithAgent = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { text: input, sender: 'user' };
        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await sendMessage(input);
            const agentMessage = { text: response.data.message, sender: 'agent' };
            setMessages((prev) => [...prev, agentMessage]);
        } catch (error) {
            const errorMessage = { text: 'Error sending message', sender: 'agent' };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const chatContainer = document.getElementById('chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="chat-container" id="chat-container">
            <div className="messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
                {loading && <div className="message agent">Typing...</div>}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Type your message..."
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
};

export default ChatWithAgent;