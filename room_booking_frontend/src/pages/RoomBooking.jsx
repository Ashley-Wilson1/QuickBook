import React, { useState, useEffect } from "react";
import RoomBookingForm from "../components/RoomBookingForm";
import "../styles/RoomBooking.css";
import NavBar from "../components/NavBar";
import api from "../api";
import Footer from "../components/Footer";

function RoomBooking() {
	const [isVerified, setIsVerified] = useState(null);

	useEffect(() => {
		api.get("/members/user/profile/")
			.then((response) => setIsVerified(response.data.verified))
			.catch((error) => console.error("Error fetching user status:", error));
	}, []);

	if (isVerified === null) {
		return <p>Loading...</p>;
	}

	if (!isVerified) {
		return (
			<div className="home">
				<NavBar />
				<div className="home-content">
					<div className="error-message">
						<p>You cannot book a room as you are not a verified user. Please contact an admin.</p>
					</div>
				</div>
				<Footer />
			</div>
		);
	}
	return (
		<div className="home">
			<NavBar />
			<div className="home-content">
				<RoomBookingForm />
			</div>
			<Footer />
		</div>
	);
}

export default RoomBooking;
