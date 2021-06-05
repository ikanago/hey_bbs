import React, { useEffect, useReducer, useState } from "react";
import { AuthContext } from "./context";
import { authReducer } from "./context";
import { baseUrl, endpoint } from "../const";

type Props = {
    children?: React.ReactNode;
};

const AuthProvider: React.FC = (props: Props) => {
    const [state, dispatch] = useReducer(authReducer, { user: undefined });

    useEffect(() => {
        (async () => {
            const res = await fetch(`${baseUrl}/${endpoint.verifyLogin}`, {
                method: "GET",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
            });
            if (!res.ok) {
                return;
            }
            const json = await res.json();
            dispatch({ type: "authenticate", nextState: json });
        })();
    }, []);

    return (
        <AuthContext.Provider value={{ state, dispatch }}>
            {props.children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;
