import React, { useState, useEffect } from "react";
import ChatLog from "./ChatLog";
import api from "../api";
function ChatBox({ bookingId }) {
	const [messages, setMessages] = useState([]);
	const [newMessage, setNewMessage] = useState("");

	useEffect(() => {
		api.get(`/chat/bookings/${bookingId}/messages/`)
			.then((response) => {
				setMessages(response.data);
			})
			.catch((error) => {
				console.error("Error fetching messages:", error);
			});
	}, [bookingId]);

	const sendMessage = async () => {
		if (!newMessage.trim()) return;

		try {
			const response = await api.post(`/chat/bookings/${bookingId}/messages/send/`, {
				text: newMessage,
			});
			setMessages([...messages, response.data]); // Append new message to chat log
			setNewMessage(""); // Clear input field
		} catch (error) {
			console.error("Error sending message:", error);
		}
	};

	return (
		<div className="chat-box">
			<h3>Chat</h3>
			<ChatLog messages={messages} />
			<input type="text" value={newMessage} onChange={(e) => setNewMessage(e.target.value)} placeholder="Type a message..." />
			<button onClick={sendMessage}>Send</button>
		</div>
	);
}

export default ChatBox;
