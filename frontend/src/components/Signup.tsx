import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import { baseUrl } from "../config";

const Signup: React.FC = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [hasSignupFailed, setHasSignupFailed] = useState(false);
    let history = useHistory();

    const submit = async () => {
        try {
            const res = await fetch(`${baseUrl}/signup`, {
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
            if (res.status >= 400) {
                throw new Error();
            }
            history.push("/posts");
        } catch (e) {
            setHasSignupFailed(true);
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
                Sign up
            </button>
            {hasSignupFailed ? <p>Sign up failed.</p> : <></>}
        </form>
    );
};

export default Signup;
