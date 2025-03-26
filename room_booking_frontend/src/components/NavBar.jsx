import { useState, useEffect } from "react";
import api from "../api";
import { Link, useNavigate } from "react-router-dom";
import "../styles/NavBar.css";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

function NavBar() {
	const [user, setUser] = useState(null);
	const navigate = useNavigate();

	useEffect(() => {
		const fetchUser = async () => {
			try {
				const res = await api.get("/members/user/profile/");
				setUser(res.data);
			} catch (error) {
				console.error("Error fetching user details:", error);
			}
		};

		fetchUser();
	}, []);

	const handleLogout = () => {
		localStorage.removeItem(ACCESS_TOKEN, REFRESH_TOKEN);

		navigate("/logout");
	};

	return (
		<nav className="navbar">
			<div className="nav-left">
				<Link to="/" className="nav-logo">
					QuickBook
				</Link>
				<Link to="/RoomBooking" className="nav-link">
					Book a room
				</Link>
			</div>

			<div className="nav-right">
				{user ? (
					<>
						<span className="nav-user">{user.first_name || user.username}</span>
						<button onClick={handleLogout} className="nav-button">
							Logout
						</button>
					</>
				) : (
					<Link to="/login" className="nav-link">
						Login
					</Link>
				)}
			</div>
		</nav>
	);
}

export default NavBar;
