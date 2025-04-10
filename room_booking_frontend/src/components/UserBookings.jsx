import { useEffect, useState } from "react";
import api from "../api";
import BookingList from "../components/BookingList";

function UserBookings() {
	const [currentBookings, setCurrentBookings] = useState([]);
	const [oldBookings, setOldBookings] = useState([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState("");

	useEffect(() => {
		const fetchBookings = async () => {
			try {
				const res = await api.get("room_booking/user/bookings/");
				setCurrentBookings(res.data.current_bookings);
				setOldBookings(res.data.old_bookings);
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
		console.log(error);
		return <p>{error}</p>;
	}

	return (
		<div className="user-bookings">
			<BookingList bookings={currentBookings} title="Your Current Bookings" />
			<BookingList bookings={oldBookings} title="Your Old Bookings" />
		</div>
	);
}

export default UserBookings;
