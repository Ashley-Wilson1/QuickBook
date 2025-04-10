import React from "react";
import "../styles/BookingList.css";
import { useNavigate } from "react-router-dom";

function BookingList({ bookings, title }) {
	const navigate = useNavigate();

	// Sort bookings by start time in ascending order
	const sortedBookings = bookings.sort((a, b) => {
		const dateA = new Date(a.start_datetime);
		const dateB = new Date(b.start_datetime);
		return dateA - dateB;
	});

	return (
		<div className="booking-list">
			<h2>{title}</h2>
			{bookings.length === 0 ? (
				<p>No bookings available.</p>
			) : (
				<table>
					<thead>
						<tr>
							<th>Room Number</th>
							<th>Building</th>
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
								<td>{booking.room.building}</td>
								<td>{booking.purpose || "No purpose specified"}</td>
								<td>{new Date(booking.start_datetime).toLocaleString()}</td>
								<td>{new Date(booking.end_datetime).toLocaleString()}</td>
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
