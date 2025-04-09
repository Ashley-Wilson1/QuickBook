import React, { useState, useEffect } from "react";
import RoomBookingForm from "../components/RoomBookingForm";
import "../styles/RoomBooking.css";
import NavBar from "../components/NavBar"; // Ensure NavBar is imported
import api from "../api"; // Ensure your API utility is imported

function RoomBooking() {
	const [isVerified, setIsVerified] = useState(null);

	useEffect(() => {
		api.get("/members/user/profile/")
			.then((response) => setIsVerified(response.data.verified))
			.catch((error) => console.error("Error fetching user status:", error));

		console.log();
	}, []);

	if (isVerified === null) {
		return <p>Loading...</p>;
	}

	if (!isVerified) {
		return (
			<>
				<NavBar />
				<div className="error-message">
					<p>You cannot book a room as you are not a verified user. Please contact an admin.</p>
				</div>
			</>
		);
	}

	return (
		<>
			<NavBar />
			<RoomBookingForm />
		</>
	);
}

export default RoomBooking;
