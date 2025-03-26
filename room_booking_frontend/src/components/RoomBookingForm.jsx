import { useState, useEffect } from "react";
import api from "../api";
import "../styles/Booking.css";

function RoomBookingForm() {
	const [rooms, setRooms] = useState([]);
	const [room, setRoom] = useState("");
	const [startDateTime, setStartDateTime] = useState("");
	const [endDateTime, setEndDateTime] = useState("");
	const [error, setError] = useState("");
	const [success, setSuccess] = useState("");
	const [userSearchResults, setUserSearchResults] = useState([]);
	const [userSearch, setUserSearch] = useState("");
	const [selectedUsers, setSelectedUsers] = useState([]);
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

	useEffect(() => {
		const fetchRooms = async () => {
			try {
				const res = await api.get("/room_booking/rooms/");
				setRooms(res.data);
			} catch (error) {
				console.error("Error fetching rooms:", error);
			}
		};

		fetchRooms();
	}, []);

	const handleUserSearch = async (e) => {
		setUserSearch(e.target.value);
		try {
			if (e.target.value) {
				const res = await api.get(`/members/user/search/?email=${e.target.value}`);
				setUserSearchResults(res.data);
			} else {
				setUserSearchResults([]);
			}
		} catch (error) {
			console.error("Error fetching user search results:", error);
		}
	};

	// Add user to selected users list
	const handleAddUser = (user) => {
		if (!selectedUsers.some((u) => u.id === user.id)) {
			setSelectedUsers([...selectedUsers, user]);
		}
	};

	const handleSubmit = async (e) => {
		e.preventDefault();
		setError("");
		setSuccess("");

		if (!room || !startDateTime || !endDateTime) {
			setError("All fields are required.");
			return;
		}

		const loggedInUserId = user.id;

		if (!loggedInUserId) {
			setError("Logged in user ID not found.");
			return;
		}

		// Add the logged-in user to the list of users
		const usersToSubmit = [loggedInUserId, ...selectedUsers.map((user) => user.id)]; // Ensure you're sending user IDs

		// Log the request data for debugging
		console.log("Request Data:", {
			room_id: room,
			start_datetime: startDateTime,
			end_datetime: endDateTime,
			users: usersToSubmit,
		});

		try {
			const res = await api.post("/room_booking/bookings/", {
				room_id: room,
				start_datetime: startDateTime,
				end_datetime: endDateTime,
				users: usersToSubmit,
			});

			setSuccess("Booking created successfully!");
			setRoom("");
			setStartDateTime("");
			setEndDateTime("");
			setSelectedUsers([]); // Clear selected users after successful booking
		} catch (error) {
			let errorMessage = "An unknown error occurred. Please try again.";

			// Check if error.response and error.response.data are available
			if (error.response && error.response.data) {
				const errorData = error.response.data.error;

				if (Array.isArray(errorData)) {
					errorMessage = errorData.join(" ");
				} else if (typeof errorData === "string") {
					errorMessage = errorData;
				} else if (errorData && typeof errorData === "object") {
					errorMessage = Object.values(errorData).flat().join(" ");
				}
			}

			// Handle specific error cases
			if (errorMessage.includes("This room is already booked for the selected time.")) {
				setError("This room is already booked for the selected time.");
			} else if (errorMessage.includes("Start time must be before end time.")) {
				setError("Start time must be before end time.");
			} else {
				setError(errorMessage); // Generic error message
			}
		}
	};

	return (
		<div className="room-booking-form">
			<h2>Book a Room</h2>
			{error && <p className="error-message">{error}</p>}
			{success && <p style={{ color: "green" }}>{success}</p>}
			<form onSubmit={handleSubmit}>
				<label>Room:</label>
				<select value={room} onChange={(e) => setRoom(e.target.value)} required>
					<option value="">Select a room</option>
					{rooms.map((r) => (
						<option key={r.id} value={r.id}>
							Room {r.number} (Capacity: {r.capacity})
						</option>
					))}
				</select>

				<label>Start Time:</label>
				<input type="datetime-local" value={startDateTime} onChange={(e) => setStartDateTime(e.target.value)} required />

				<label>End Time:</label>
				<input type="datetime-local" value={endDateTime} onChange={(e) => setEndDateTime(e.target.value)} required />

				<label>Search for Users by Email:</label>
				<input type="text" value={userSearch} onChange={handleUserSearch} placeholder="Search by email" />
				<ul>
					{userSearchResults.map((user) => (
						<li key={user.id} onClick={() => handleAddUser(user)}>
							{user.email} - {user.first_name} {user.last_name}
						</li>
					))}
				</ul>

				<h4>Selected Users:</h4>
				<ul>
					{selectedUsers.map((user) => (
						<li key={user.id}>{user.email}</li>
					))}
				</ul>

				<button type="submit">Book Room</button>
			</form>
		</div>
	);
}

export default RoomBookingForm;
