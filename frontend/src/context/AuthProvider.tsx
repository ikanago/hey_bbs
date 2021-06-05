import React, { useEffect, useState } from "react";
import { AuthContext } from "./context";
import type { UserInfo } from "./context";
import { baseUrl, endpoint } from "../const";

type Props = {
    children?: React.ReactNode;
};

const AuthProvider: React.FC = (props: Props) => {
    const [user, setUser] = useState<UserInfo | undefined>(undefined);

    useEffect(() => {
        (async () => {
            try {
                const res = await fetch(`${baseUrl}/${endpoint.verifyLogin}`, {
                    method: "GET",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });
                if (!res.ok) {
                    throw new Error();
                }
                const json = await res.json();
                setUser(json);
            } catch (e) {
                setUser(undefined);
            }
        })();
    }, []);

    return (
        <AuthContext.Provider
            value={{ state: { userInfo: user }, dispatch: setUser }}
        >
            {props.children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;
