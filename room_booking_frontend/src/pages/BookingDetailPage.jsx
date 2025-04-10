import React from "react";
import BookingDetails from "../components/BookingDetails";
import NavBar from "../components/NavBar";
import Footer from "../components/Footer";

function BookingDetailPage({ bookingId }) {
	return (
		<div className="home">
			<NavBar />
			<div className="home-content">
				<BookingDetails bookingId={bookingId} />
			</div>
			<Footer />
		</div>
	);
}
export default BookingDetailPage;
