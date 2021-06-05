import React, { useState } from "react";
import { useHistory } from "react-router-dom";

const Signup: React.FC = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    let history = useHistory();

    const url = "http://localhost:3000/signup";
    const submit = async () => {
        try {
            const res = await fetch(url, {
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
                throw new Error(`HTTP error: ${res.status}`);
            }
            history.push("/posts");
        } catch (e) {
            console.error(e);
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
        </form>
    );
};

export default Signup;
