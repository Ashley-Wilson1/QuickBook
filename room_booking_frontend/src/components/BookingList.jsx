import React from "react";
import "../styles/BookingList.css";

function BookingList({ bookings }) {
	return (
		<div className="booking-list">
			<h2>Your Room Bookings</h2>
			{bookings.length === 0 ? (
				<p>No bookings available</p>
			) : (
				<table>
					<thead>
						<tr>
							<th>Room Number</th>
							<th>Start Time</th>
							<th>End Time</th>
							<th>Users</th>
						</tr>
					</thead>
					<tbody>
						{bookings.map((booking) => (
							<tr key={booking.id}>
								<td>{booking.room.number}</td>
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
