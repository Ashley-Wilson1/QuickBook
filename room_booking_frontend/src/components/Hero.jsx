import React from "react";
import "../styles/Hero.css";

function Hero() {
	return (
		<div className="hero">
			<h1>Welcome to Leeds Beckett Room Booking</h1>
			<p>Book rooms and manage your bookings with ease.</p>
			<button onClick={() => (window.location.href = "/RoomBooking")}>Get Started, Book a Room</button>
		</div>
	);
}

export default Hero;
