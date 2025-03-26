import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import ChatBox from "./ChatBox";

function BookingDetails() {
	const { bookingId } = useParams();

	return (
		<div>
			<h2>Booking Details</h2>

			<ChatBox bookingId={bookingId} />
		</div>
	);
}

export default BookingDetails;
