import React from "react";
import NavBar from "../components/NavBar";
import UserBookings from "../components/UserBookings";
import Hero from "../components/Hero";
import Footer from "../components/Footer";
import "../styles/Home.css";

function Home() {
	return (
		<div className="home">
			<NavBar />
			<div className="home-content">
				<Hero />
				<UserBookings />
			</div>
			<Footer />
		</div>
	);
}

export default Home;
