import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";

export const Profile = () => {
    const { store, actions } = useContext(Context);
    

    useEffect(()=>{
        actions.getProfile()
    },[])

    return (
        <div className="text-center mt-5">
            <h1>Profile</h1>
            <p className="p-3 mb-2 bg-info text-dark">Has iniciado sesión con el siguente email: {store.user ? store.user.email : 'cargando...'}</p>
        </div>
    );
};
