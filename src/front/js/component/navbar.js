import React, {useContext} from "react";
import { Context } from "../store/appContext";
import { Link, useNavigate } from "react-router-dom";

export const Navbar = () => {
	const { store, actions } = useContext(Context);
    const navigate = useNavigate(); 
	const handleLogout = () => { // Definir handleLogout AQUÍ, dentro del componente
        actions.logout();
        navigate("/");
    };

	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">React Boilerplate</span>
				</Link>
				<div className="ml-auto">
					{store.auth ? (
                        <>    
							<Link to="/demo">
                                <button className="btn btn-primary me-2">Check the Context in action</button> 
                            </Link>
							<button className="btn btn-danger" onClick={handleLogout}>Logout</button>
						</>
                    ) : null}
					<Link to="/signup">
                            <button className="btn btn-primary me-2">Register</button> 
                    </Link>
				</div>
			</div>
		</nav>
	);
};
