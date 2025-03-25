import { useState, useEffect } from "react";
import api from "../api";

function NavBar() {
	const [user, setUser] = useState(null);

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

	return (
		<nav>
			<div>
				<a href="/">QuickBook</a>
			</div>

			<div>
				<a href="/room_booking">Room Booking</a>
			</div>

			<div>
				{user ? (
					<>
						<span>{user.first_name || user.username}</span>
						<button>Logout</button>
					</>
				) : (
					<a href="/login">Login</a>
				)}
			</div>
		</nav>
	);
}

export default NavBar;
