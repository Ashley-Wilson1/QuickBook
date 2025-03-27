import React from "react";
import "../styles/BookingList.css";
import { useNavigate } from "react-router-dom";

function BookingList({ bookings }) {
	const navigate = useNavigate();

	const sortedBookings = bookings.sort((a, b) => {
		const dateA = new Date(a.start_datetime);
		const dateB = new Date(b.start_datetime);
		return dateA - dateB; // Sort in ascending order
	});

	return (
		<div className="booking-list">
			<h2>Your Room Bookings</h2>
			{bookings.length === 0 ? (
				<p>You have no bookings yet.</p>
			) : (
				<table>
					<thead>
						<tr>
							<th>Room Number</th>
							<th>Purpose</th>
							<th>Start Time</th>
							<th>End Time</th>
							<th>Users</th>
						</tr>
					</thead>
					<tbody>
						{sortedBookings.map((booking) => (
							<tr key={booking.id} onClick={() => navigate(`/booking/${booking.id}`)} style={{ cursor: "pointer" }}>
								<td>{booking.room.number}</td>
								<td>{booking.purpose}</td>
								<td>{new Date(booking.start_datetime).toISOString().replace("T", " ").substring(0, 16)}</td>
								<td>{new Date(booking.end_datetime).toISOString().replace("T", " ").substring(0, 16)}</td>
								<td>
									<ul>
										{booking.users.map((user) => (
											<li key={user.id}>
												{user.first_name} {user.last_name} ({user.email})
											</li>
										))}
									</ul>
								</td>
							</tr>
						))}
					</tbody>
				</table>
			)}
		</div>
	);
}

export default BookingList;
