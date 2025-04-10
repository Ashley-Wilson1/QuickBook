import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import "../styles/Form.css";

function RegisterForm({ route }) {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [email, setEmail] = useState("");
	const [firstName, setFirstName] = useState("");
	const [lastName, setLastName] = useState("");
	const [userType, setUserType] = useState("student");
	const [errors, setErrors] = useState({});
	const [loading, setLoading] = useState(false);
	const navigate = useNavigate();

	const handleSubmit = async (e) => {
		setLoading(true);
		e.preventDefault();

		try {
			const res = await api.post(route, {
				username,
				password,
				first_name: firstName,
				last_name: lastName,
				email,
				user_type: userType,
			});
			navigate("/login");
		} catch (error) {
			if (error.response && error.response.data) {
				setErrors(error.response.data);
			} else {
				setErrors({ general: "Registration failed. Please try again." });
			}
		} finally {
			setLoading(false);
		}
	};

	return (
		<form onSubmit={handleSubmit} className="form-container">
			<h1>Register</h1>
			{errors.username && <p className="error-message">{errors.username[0]}</p>}
			<input className="form-input" type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
			{errors.email && <p className="error-message">{errors.email[0]}</p>}
			<input className="form-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
			<input className="form-input" type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} placeholder="First Name" />
			<input className="form-input" type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} placeholder="Last Name" />
			<select className="form-input" value={userType} onChange={(e) => setUserType(e.target.value)} required>
				<option value="student">Student</option>
				<option value="staff">Staff</option>
			</select>
			<input
				className="form-input"
				type="password"
				value={password}
				onChange={(e) => setPassword(e.target.value)}
				placeholder="Password"
				required
			/>
			{errors.general && <p className="error-message">{errors.general}</p>}
			<button className="form-button" type="submit">
				Register
			</button>

			<p>
				Already have an account? You can <a href="/login">Login here</a>.
			</p>
		</form>
	);
}

export default RegisterForm;
