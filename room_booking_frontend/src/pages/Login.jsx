import LoginForm from "../components/LoginForm";
import Footer from "../components/Footer";
import "../styles/Auth.css";

function Login() {
	return (
		<div className="auth-page">
			<div className="auth-content">
				<LoginForm route="members/token/" />
			</div>
			<Footer />
		</div>
	);
}

export default Login;
