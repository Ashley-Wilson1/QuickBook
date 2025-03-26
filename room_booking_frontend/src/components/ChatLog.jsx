import React from "react";

function ChatLog({ messages }) {
	return (
		<div className="chat-log">
			{messages.length === 0 ? (
				<p>No messages yet.</p>
			) : (
				messages.map((msg, index) => (
					<p key={index}>
						<strong>{msg.user.username}:</strong> {msg.text}
					</p>
				))
			)}
		</div>
	);
}

export default ChatLog;
