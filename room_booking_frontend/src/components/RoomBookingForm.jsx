import { useState, useEffect } from "react";
import api from "../api"; // Ensure this handles JWT authentication
import "../styles/Booking.css";

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
				room_id: room,
				start_datetime: startDateTime,
				end_datetime: endDateTime,
			});

			setSuccess("Booking created successfully!");
			setRoom("");
			setStartDateTime("");
			setEndDateTime("");
		} catch (error) {
			let errorMessage = "An unknown error occurred. Please try again.";

			// Check if error.response and error.response.data are available
			if (error.response && error.response.data) {
				const errorData = error.response.data.error;

				if (Array.isArray(errorData)) {
					// If errorData is an array, join the messages into one string
					errorMessage = errorData.join(" ");
				} else if (typeof errorData === "string") {
					// If errorData is a string, use it directly
					errorMessage = errorData;
				} else if (errorData && typeof errorData === "object") {
					// If errorData is an object, handle its values (could be field errors)
					errorMessage = Object.values(errorData).flat().join(" "); // Flatten array values and join them
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

				<button type="submit">Book Room</button>
			</form>
		</div>
	);
}

export default RoomBookingForm;
