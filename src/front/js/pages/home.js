import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import { LoginForm } from "../component/loginForm";
import "../../styles/home.css";
import { Navbar } from "../component/navbar";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="text-center mt-5">
			<Navbar/>
			<h1>Hello Rigo!!</h1>
			<LoginForm/>
		</div>
	);
};
