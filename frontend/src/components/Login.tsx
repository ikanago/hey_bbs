import React, { useContext, useState } from "react";
import { useHistory } from "react-router-dom";
import { baseUrl } from "../const";
import { AuthContext } from "../context/context";

const Login: React.FC = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [logInError, setLogInError] = useState<string | undefined>(undefined);
    const { dispatch } = useContext(AuthContext);
    let history = useHistory();

    const submit = async () => {
        try {
            const res = await fetch(`${baseUrl}/login`, {
                method: "POST",
                mode: "cors",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });
            if (!res.ok) {
                throw new Error();
            }
            dispatch({
                type: "authenticate",
                nextState: {
                    user: {
                        username: username,
                    },
                },
            });
            history.push("/posts");
        } catch (e) {
            setLogInError(
                "ユーザ名かパスワードが間違っています．もう一度お試しください．"
            );
        }
    };

    return (
        <form>
            <input
                onChange={event => setUsername(event.target.value)}
                value={username}
                type="text"
            />
            <input
                onChange={event => setPassword(event.target.value)}
                value={password}
                type="password"
            />
            <button
                onClick={e => {
                    e.preventDefault();
                    submit();
                }}
            >
                Log in
            </button>
            {logInError ? <p>{logInError}</p> : <></>}
        </form>
    );
};

export default Login;
