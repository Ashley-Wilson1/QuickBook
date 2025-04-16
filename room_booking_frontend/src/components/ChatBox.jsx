import React, { useState, useEffect, useRef } from "react";
import { ACCESS_TOKEN } from "../constants";
import api from "../api";

const ChatBox = ({ bookingId }) => {
	const [messages, setMessages] = useState([]);
	const [newMessage, setNewMessage] = useState("");
	const token = localStorage.getItem(ACCESS_TOKEN);
	const socketRef = useRef(null);

	useEffect(() => {
		const fetchMessages = async () => {
			try {
				const response = await api.get(`chat/${bookingId}/history/`);
				const data = response.data.messages || [];
				setMessages(data);
			} catch (error) {
				console.error("Failed to fetch chat history:", error);
				setMessages([]);
			}
		};

		fetchMessages();

		socketRef.current = new WebSocket(`${import.meta.env.VITE_API_URL.replace("http", "ws")}/ws/chat/${bookingId}/?token=${token}`);

		socketRef.current.onopen = () => {
			console.log("WebSocket connection established");
		};

		socketRef.current.onmessage = (event) => {
			const data = JSON.parse(event.data);
			if (data.error) {
				console.error(data.error);
			} else {
				setMessages((prevMessages) => [...prevMessages, data]);
			}
		};

		return () => {
			if (socketRef.current) {
				socketRef.current.close();
			}
		};
	}, [bookingId, token]);

	const sendMessage = () => {
		if (newMessage.trim()) {
			if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
				const messageData = {
					text: newMessage,
				};
				socketRef.current.send(JSON.stringify(messageData));
				setNewMessage("");
			} else {
				console.error("WebSocket is not open. Message not sent.");
			}
		}
	};

	return (
		<div className="chat-box">
			<div className="messages">
				{!messages || messages.length === 0 ? (
					<p>No messages yet. Start the conversation!</p>
				) : (
					messages.map((msg, index) => (
						<div key={index} className="message">
							<strong>{msg.user?.username || "Unknown"}:</strong> {msg.text || "No message content"}
						</div>
					))
				)}
			</div>
			<div className="message-input">
				<input type="text" value={newMessage} onChange={(e) => setNewMessage(e.target.value)} placeholder="Type your message..." />
				<button onClick={sendMessage}>Send</button>
			</div>
		</div>
	);
};

export default ChatBox;
