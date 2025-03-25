import { useState, useEffect } from "react";
import api from "../api"; // Ensure this handles JWT authentication

function RoomBookingForm() {
	const [rooms, setRooms] = useState([]);
	const [room, setRoom] = useState("");
	const [startDateTime, setStartDateTime] = useState("");
	const [endDateTime, setEndDateTime] = useState("");
	const [error, setError] = useState("");
	const [success, setSuccess] = useState("");

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

	const handleSubmit = async (e) => {
		e.preventDefault();
		setError("");
		setSuccess("");

		if (!room || !startDateTime || !endDateTime) {
			setError("All fields are required.");
			return;
		}

		try {
			const res = await api.post("/room_booking/bookings/", {
				room,
				start_datetime: startDateTime,
				end_datetime: endDateTime,
			});

			setSuccess("Booking created successfully!");
			setRoom("");
			setStartDateTime("");
			setEndDateTime("");
		} catch (error) {
			const errorMessage = error.response?.data?.error || "An error occurred. Please try again.";
			setError(errorMessage);
		}
	};

	return (
		<div>
			<h2>Book a Room</h2>
			{error && <p style={{ color: "red" }}>{error}</p>}
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

				<button type="submit">Book Room</button>
			</form>
		</div>
	);
}

export default RoomBookingForm;
