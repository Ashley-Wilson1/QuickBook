import React from "react";
import NavBar from "../components/NavBar";
import UserBookings from "../components/UserBookings";

function Home() {
	return (
		<div>
			<NavBar />
			<h1> Dashboard</h1>
			<UserBookings />
		</div>
	);
}

export default Home;
