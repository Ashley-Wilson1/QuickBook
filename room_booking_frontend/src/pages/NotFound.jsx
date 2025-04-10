import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/NotFound.css";

function NotFound() {
	const navigate = useNavigate();

	return (
		<div className="not-found-container">
			<h1>404</h1>
			<p>The page you are looking for does not exist.</p>
			<button onClick={() => navigate("/")}>Go Back to Homepage</button>
		</div>
	);
}

export default NotFound;
