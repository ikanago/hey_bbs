import React, { useEffect, useReducer } from "react";
import { AuthContext } from "./context";
import { authReducer } from "./context";
import { verifyLogin } from "../api";

type Props = {
    children?: React.ReactNode;
};

const AuthProvider: React.FC = (props: Props) => {
    const [state, dispatch] = useReducer(authReducer, { user: undefined });

    useEffect(() => {
        (async () => {
            const json = await verifyLogin();
            dispatch({
                type: "authenticate",
                nextState: { user: { username: json } },
            });
        })();
    }, []);

    return (
        <AuthContext.Provider value={{ state, dispatch }}>
            {props.children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;
