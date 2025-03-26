import { useEffect, useState } from "react";
import api from "../api";
import BookingList from "../components/BookingList";

function UserBookings() {
	const [bookings, setBookings] = useState([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState("");

	useEffect(() => {
		const fetchBookings = async () => {
			try {
				const res = await api.get("room_booking/user/bookings/");

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

	return <div className="user-bookings">{bookings.length > 0 ? <BookingList bookings={bookings} /> : <p>No bookings found.</p>}</div>;
}

export default UserBookings;
