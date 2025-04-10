import RegisterForm from "../components/RegisterForm";
import Footer from "../components/Footer";
import "../styles/Auth.css";

function Register() {
	return (
		<div className="auth-page">
			<div className="auth-content">
				<RegisterForm route="members/user/register/" />
			</div>
			<Footer />
		</div>
	);
}

export default Register;
