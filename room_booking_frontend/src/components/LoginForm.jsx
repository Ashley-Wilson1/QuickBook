import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/Form.css";

function LoginForm({ route }) {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [loading, setLoading] = useState(false);
	const [errors, setErrors] = useState({ username: "", password: "", general: "" });

	const navigate = useNavigate();

	const handleSubmit = async (e) => {
		setLoading(true);
		e.preventDefault();

		try {
			const res = await api.post(route, { username, password });
			localStorage.setItem(ACCESS_TOKEN, res.data.access);
			localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
			navigate("/");
		} catch (error) {
			if (error.response && error.response.data) {
				const errorMessage = error.response.data.error || error.response.data.detail;

				if (errorMessage.includes("No active account found")) {
					setErrors({ username: "", password: "Incorrect username or password.", general: "" });
				} else if (errorMessage.includes("Username does not exist")) {
					setErrors({ username: errorMessage, password: "", general: "" });
				} else {
					setErrors({ username: "", password: "", general: "Login failed. Please try again." });
				}
			} else {
				setErrors({ username: "", password: "", general: "Something went wrong. Please try again later." });
			}
		} finally {
			setLoading(false);
		}
	};

	return (
		<form onSubmit={handleSubmit} className="form-container">
			<h1>Login</h1>
			{errors.username && <p className="error-message">{errors.username}</p>}
			{errors.general && <p className="error-message">{errors.general}</p>}
			{errors.password && <p className="error-message">{errors.password}</p>}
			<input className="form-input" type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />

			<input className="form-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />

			<button className="form-button" type="submit">
				Login
			</button>
			<p>
				Don't Have an account? You can <a href="/register">Sign up here</a>.
			</p>
		</form>
	);
}

export default LoginForm;
