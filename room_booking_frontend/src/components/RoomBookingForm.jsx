import { useState, useEffect } from "react";
import api from "../api";
import "../styles/Booking.css";
import "react-calendar/dist/Calendar.css";

function RoomBookingForm() {
	const [rooms, setRooms] = useState([]);
	const [selectedRoom, setSelectedRoom] = useState("");
	const [startDateTime, setStartDateTime] = useState("");
	const [endDateTime, setEndDateTime] = useState("");
	const [duration, setDuration] = useState(1);
	const [error, setError] = useState("");
	const [success, setSuccess] = useState("");
	const [userSearchResults, setUserSearchResults] = useState([]);
	const [userSearch, setUserSearch] = useState("");
	const [selectedUsers, setSelectedUsers] = useState([]);
	const [user, setUser] = useState(null);
	const [purpose, setPurpose] = useState("");
	const [selectedDate, setSelectedDate] = useState(new Date());
	const [availableTimes, setAvailableTimes] = useState([]);
	const [selectedTimeSlot, setSelectedTimeSlot] = useState(null);
	const [buildings, setBuildings] = useState([]);
	const [selectedBuilding, setSelectedBuilding] = useState("");

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
		api.get("/room_booking/buildings/")
			.then((response) => setBuildings(response.data))
			.catch((error) => console.error("Error fetching buildings:", error));
	}, []);

	useEffect(() => {
		if (selectedBuilding) {
			api.get(`/room_booking/rooms/?building=${selectedBuilding}`)
				.then((response) => setRooms(response.data))
				.catch((error) => console.error("Error fetching rooms:", error));
		} else {
			setRooms([]);
		}
	}, [selectedBuilding]);

	const handleBuildingChange = (e) => {
		setSelectedBuilding(e.target.value);
		setSelectedRoom("");
	};

	const handleRoomChange = (e) => {
		setSelectedRoom(e.target.value);
	};

	useEffect(() => {
		const fetchAvailableTimes = async () => {
			if (selectedRoom && selectedDate) {
				try {
					const res = await api.get(`/room_booking/available_times/?room_id=${selectedRoom}&date=${selectedDate.toISOString().split("T")[0]}`);
					setAvailableTimes(res.data);
				} catch (error) {
					console.error("Error fetching available times:", error);
				}
			}
		};

		fetchAvailableTimes();
	}, [selectedRoom, selectedDate]);

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

	const handleAddUser = (user) => {
		if (!selectedUsers.some((u) => u.id === user.id)) {
			setSelectedUsers([...selectedUsers, user]);
			setUserSearch("");
			setUserSearchResults([]);
		}
	};

	const handleRemoveUser = (userId) => {
		setSelectedUsers(selectedUsers.filter((user) => user.id !== userId));
	};

	const handleTimeSlotSelect = (timeSlot) => {
		const selectedDateTime = new Date(`${selectedDate.toISOString().split("T")[0]}T${timeSlot.start}:00Z`);
		const endTime = new Date(selectedDateTime);
		endTime.setHours(selectedDateTime.getHours() + duration);

		let isAvailable = true;
		let currentTime = new Date(selectedDateTime);

		for (let i = 0; i < duration; i++) {
			const currentHour = currentTime.toISOString().split("T")[1].slice(0, 5);
			if (!availableTimes.some((slot) => slot.start === currentHour)) {
				isAvailable = false;
				break;
			}
			currentTime.setHours(currentTime.getHours() + 1);
		}

		if (!isAvailable) {
			setError("Selected duration is not fully available.");
			return;
		}

		setStartDateTime(selectedDateTime.toISOString().slice(0, 16));
		setEndDateTime(endTime.toISOString().slice(0, 16));
		setSelectedTimeSlot({ start: selectedDateTime, end: endTime });
		setError("");
	};

	const isTimeSlotSelected = (timeSlot) => {
		if (!selectedTimeSlot) return false;

		const timeSlotStart = new Date(`${selectedDate.toISOString().split("T")[0]}T${timeSlot.start}:00Z`);

		return timeSlotStart >= selectedTimeSlot.start && timeSlotStart < selectedTimeSlot.end;
	};

	const handleSubmit = async (e) => {
		e.preventDefault();
		setError("");
		setSuccess("");

		if (!selectedRoom || !startDateTime || !endDateTime || !purpose) {
			setError("All fields are required.");
			return;
		}

		const loggedInUserId = user.id;

		if (!loggedInUserId) {
			setError("Logged in user ID not found.");
			return;
		}

		const usersToSubmit = [loggedInUserId, ...selectedUsers.map((user) => user.id)];

		try {
			const res = await api.post("/room_booking/bookings/", {
				room_id: selectedRoom,
				start_datetime: startDateTime,
				end_datetime: endDateTime,
				users: usersToSubmit,
				purpose: purpose,
			});

			setSuccess("Booking created successfully!");
			setSelectedRoom("");
			setStartDateTime("");
			setEndDateTime("");
			setPurpose("");
			setSelectedUsers([]);
		} catch (error) {
			let errorMessage = "An unknown error occurred. Please try again.";

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

			if (errorMessage.includes("This room is already booked for the selected time.")) {
				setError("This room is already booked for the selected time.");
			} else if (errorMessage.includes("Start time must be before end time.")) {
				setError("Start time must be before end time.");
			} else {
				setError(errorMessage);
			}
		}
	};

	const convertToLocalTime = (isoString) => {
		const date = new Date(isoString);
		date.setHours(date.getHours() - 1);
		return date.toLocaleString();
	};

	const convertAvailableTime = (timeSlot) => {
		const start = new Date(`${selectedDate.toISOString().split("T")[0]}T${timeSlot.start}:00Z`);
		const end = new Date(`${selectedDate.toISOString().split("T")[0]}T${timeSlot.end}:00Z`);

		return {
			start: convertToLocalTime(start.toISOString()),
			end: convertToLocalTime(end.toISOString()),
		};
	};

	return (
		<div className="room-booking-container">
			<div className="timeline-container">
				<div className="timeline-header">
					<h3>Available Times</h3>
				</div>
				<div className="timeline">
					{availableTimes.length > 0 ? (
						availableTimes.map((timeSlot, index) => (
							<div
								key={index}
								className={`time-slot ${timeSlot.isAvailable ? "available" : "booked"} ${isTimeSlotSelected(timeSlot) ? "selected" : ""}`}
								onClick={() => timeSlot.isAvailable && handleTimeSlotSelect(timeSlot)}
							>
								{convertAvailableTime(timeSlot).start} - {convertAvailableTime(timeSlot).end}
							</div>
						))
					) : (
						<p>No available times for the selected date.</p>
					)}
				</div>
			</div>
			<div className="room-booking-form">
				<h2>Book a Room</h2>
				{error && <p className="error-message">{error}</p>}
				{success && <p style={{ color: "green" }}>{success}</p>}
				<form onSubmit={handleSubmit}>
					<label>Select Date:</label>
					<input
						type="date"
						value={selectedDate.toISOString().split("T")[0]}
						onChange={(e) => setSelectedDate(new Date(e.target.value))}
						required
					/>

					<label htmlFor="building">Building</label>
					<select id="building" value={selectedBuilding} onChange={handleBuildingChange}>
						<option value="">Select a building</option>
						{buildings.map((building, index) => (
							<option key={index} value={building}>
								{building}
							</option>
						))}
					</select>

					<label htmlFor="room">Room</label>
					<select id="room" value={selectedRoom} onChange={handleRoomChange} disabled={!selectedBuilding}>
						<option value="">Select a room</option>
						{rooms.map((room) => (
							<option key={room.id} value={room.id}>
								Room {room.number} (Capacity: {room.capacity})
							</option>
						))}
					</select>

					<label>Duration:</label>
					<select value={duration} onChange={(e) => setDuration(Number(e.target.value))} required>
						<option value={1}>1 Hour</option>
						<option value={2}>2 Hours</option>
						<option value={4}>4 Hours</option>
					</select>

					<label>Purpose of the Booking:</label>
					<input
						className="purpose"
						type="text"
						value={purpose}
						onChange={(e) => setPurpose(e.target.value)}
						placeholder="Enter the purpose of the booking"
						required
					/>

					<label>Search for Users by Email:</label>
					<input className="purpose" type="text" value={userSearch} onChange={handleUserSearch} placeholder="Search by email" />
					<ul className="user-search-results">
						{userSearchResults.map((user) => (
							<li key={user.id} onClick={() => handleAddUser(user)} className="user-search-result">
								{user.email} - {user.first_name} {user.last_name}
							</li>
						))}
					</ul>

					<label>Selected Users:</label>
					<ul className="selected-users">
						{selectedUsers.map((user) => (
							<li key={user.id}>
								{user.first_name} {user.last_name}
								<button type="button" onClick={() => handleRemoveUser(user.id)}>
									Remove
								</button>
							</li>
						))}
					</ul>

					<button type="submit">Book Room</button>
				</form>
			</div>
		</div>
	);
}

export default RoomBookingForm;
