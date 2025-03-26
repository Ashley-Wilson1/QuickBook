import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import ChatBox from "./ChatBox";

function BookingDetails() {
	const { bookingId } = useParams();
	const [booking, setBooking] = useState(null);

	useEffect(() => {
		if (!bookingId) return;

		api.get(`room_booking/bookings/${bookingId}/`)
			.then((response) => {
				console.log("Booking API Response:", response.data);
				setBooking(response.data);
			})
			.catch((error) => console.error("Error fetching booking:", error));
	}, [bookingId]);

	if (!booking) return <p>Loading booking details...</p>;

	return (
		<div>
			<h2>Booking Details</h2>
			<p>Room: {booking.room.number}</p>
			<p>Start Time: {new Date(booking.start_datetime).toLocaleString()}</p>
			<p>End Time: {new Date(booking.end_datetime).toLocaleString()}</p>
			<ul>
				{booking.users_detail.map((user) => (
					<li key={user.id}>
						{user.first_name} {user.last_name} ({user.email})
					</li>
				))}
			</ul>
			{/* Pass bookingId to ChatBox */}
			<ChatBox bookingId={bookingId} />
		</div>
	);
}

export default BookingDetails;
