import React from "react";
import BookingDetails from "../components/BookingDetails";
import NavBar from "../components/NavBar";

function BookingDetailPage({ bookingId }) {
	return (
		<>
			<NavBar />
			<BookingDetails bookingId={bookingId} />
		</>
	);
}
export default BookingDetailPage;
