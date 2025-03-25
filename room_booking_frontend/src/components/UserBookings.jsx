import { useEffect, useState } from "react";
import api from "../api"; // Assuming this is set up to handle JWT tokens and API calls
import BookingList from "../components/BookingList";

function UserBookings() {
	const [bookings, setBookings] = useState([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState("");

	useEffect(() => {
		const fetchBookings = async () => {
			try {
				// Replace this with the appropriate API endpoint for fetching user bookings
				const res = await api.get("/room_booking/user/bookings/");

				// Assuming the response contains the bookings in `res.data`
				setBookings(res.data);
			} catch (error) {
				setError("Error fetching bookings. Please try again later.");
				console.error("Error fetching bookings:", error);
			} finally {
				setLoading(false);
			}
		};

		fetchBookings();
	}, []);

	if (loading) {
		return <p>Loading bookings...</p>;
	}

	if (error) {
		return <p>{error}</p>;
	}

	return <BookingList bookings={bookings} />;
}

export default UserBookings;
