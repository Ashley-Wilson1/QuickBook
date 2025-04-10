import React from "react";
import "../styles/Footer.css";

function Footer() {
	return (
		<footer className="footer">
			<p>&copy; {new Date().getFullYear()} Leeds Beckett University</p>
		</footer>
	);
}

export default Footer;
