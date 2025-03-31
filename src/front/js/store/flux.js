const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			auth: false,
			user: null,
			demo: []
		},
		actions: {
			// Use getActions to call a function within a fuction
			// 
			
			signup: async (email, password) => {
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");

                const raw = JSON.stringify({
                    email: email,
                    password: password
                });

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow"
                };

                try{
					const response = await fetch("https://vigilant-funicular-q79rg7x5qxxwf4qxp-3001.app.github.dev/api/sign_up", requestOptions);
					if(response.headers.get("Content-Type")?.includes("application/json")){
						const result = await response.json();
						if (response.status === 201) {
							return true;
						}
					} else {
						console.error("Respuesta del servidor no es JSON:", await response.text());
						return false;
					}
				} catch (error) {
					console.error(error);
					return false;
				}
			},
			
			login: async (email, password) => {


				const myHeaders = new Headers();
				myHeaders.append("Content-Type", "application/json");

				const raw = JSON.stringify({
					"email": email,
					"password": password
				});

				const requestOptions = {
					method: "POST",
					headers: myHeaders,
					body: raw,
					redirect: "follow"
				};

				try {
					const response = await fetch("https://vigilant-funicular-q79rg7x5qxxwf4qxp-3001.app.github.dev/api/log_in", requestOptions);
					const result = await response.json();

					if (response.status === 200) {
						localStorage.setItem("token", result.access_token)
						setStore({ auth: true, user: { email } });
						return true
					}
				} catch (error) {
					console.error(error);
					return false;
				};
			},
			getProfile: async () => {
				let token = localStorage.getItem("token")
				try {
					const response = await fetch("https://vigilant-funicular-q79rg7x5qxxwf4qxp-3001.app.github.dev/api/profile", {
						method: "GET",
						headers: {
							"Authorization": `Bearer ${token}`
						},
					});
					const result = await response.json();
					console.log(result)
				} catch (error) {
					console.error(error);
				};
			},
			
			//crear un nuevo endpoint que se llame verificacion de token
			//la peticion en la funcion tokenVerify del front deberia actualizar un estado auth:
			tokenVerify: async () => {
                try {
                    const token = localStorage.getItem("token");
                    if (!token) {
                        setStore({ auth: false, user: null });
                        return;
                    }

                    const response = await fetch("https://vigilant-funicular-q79rg7x5qxxwf4qxp-3001.app.github.dev/api/verificacion_token", {
                        method: "GET",
                        headers: {
                            "Authorization": `Bearer ${token}`
                        },
                    });

                    const data = await response.json();
                    setStore({ auth: data.auth });
                } catch (error) {
                    console.error("No se pudo verificar el token:", error);
                    setStore({ auth: false, user: null });
                }
            },
		
			logout: () => {
                localStorage.removeItem("token");
                setStore({ auth: false, user: null });
			
			},
			// getMessage: async () => {
			// 	try {
			// 		// fetching data from the backend
			// 		const resp = await fetch(process.env.BACKEND_URL + "/api/hello")
			// 		const data = await resp.json()
			// 		setStore({ message: data.message })
			// 		// don't forget to return something, that is how the async resolves
			// 		return data;
			// 	} catch (error) {
			// 		console.log("Error loading message from backend", error)
			// 	}
			// },
			// changeColor: (index, color) => {
			// 	//get the store
			// 	const store = getStore();

			// 	//we have to loop the entire demo array to look for the respective index
			// 	//and change its color
			// 	const demo = store.demo.map((elm, i) => {
			// 		if (i === index) elm.background = color;
			// 		return elm;
			// 	});

			// 	//reset the global store
			// 	setStore({ demo: demo });
			// }
		}
	};
};

export default getState;
