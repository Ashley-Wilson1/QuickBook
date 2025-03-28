import { useState, useEffect } from "react";
import api from "../api";
import { Link, useNavigate } from "react-router-dom";
import "../styles/NavBar.css";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

function NavBar() {
	const [user, setUser] = useState(null);
	const navigate = useNavigate();
	const [notifications, setNotifications] = useState([]);
	const [showDropdown, setShowDropdown] = useState(false);

	useEffect(() => {
		const fetchUser = async () => {
			try {
				const res = await api.get("/members/user/profile/");
				setUser(res.data);
			} catch (error) {
				console.error("Error fetching user details:", error);
			}
		};

		const fetchNotifications = async () => {
			try {
				const res = await api.get("/notifications/user/");
				setNotifications(res.data);
			} catch (error) {
				console.error("Error fetching notifications:", error);
			}
		};

		fetchUser();
		fetchNotifications();
	}, []);

	const handleLogout = async () => {
		try {
			await api.post("/members/logout/");

			localStorage.removeItem(ACCESS_TOKEN);
			localStorage.removeItem(REFRESH_TOKEN);
			navigate("/login");
		} catch (error) {
			console.error("Logout failed", error);
		}
	};
	const toggleDropdown = () => {
		setShowDropdown(!showDropdown);
	};

	const markAsRead = async (id) => {
		try {
			await api.post(`/notifications/${id}/read/`);
			setNotifications((prev) => prev.map((notif) => (notif.id === id ? { ...notif, is_read: true } : notif)));
		} catch (error) {
			console.error("Error marking notification as read:", error);
		}
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
						<div className="nav-notifications">
							<button onClick={toggleDropdown} className="notif-button">
								{notifications.filter((n) => !n.is_read).length} 🔔
							</button>
							{showDropdown && (
								<div className="notif-dropdown">
									{notifications.length === 0 ? (
										<p>No notifications</p>
									) : (
										<ul>
											{notifications.map((notif) => (
												<li key={notif.id} className={notif.is_read ? "read" : "unread"} onClick={() => markAsRead(notif.id)}>
													{notif.message}
												</li>
											))}
										</ul>
									)}
								</div>
							)}
						</div>
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
