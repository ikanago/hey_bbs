import React, { useContext, useState } from "react";
import { useHistory } from "react-router-dom";
import { baseUrl, endpoint } from "../const";
import { AuthContext } from "../context/context";

const Signup: React.FC = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    // 未ログインと登録失敗を区別できていない
    const { state, dispatch } = useContext(AuthContext);
    let history = useHistory();

    const submit = async () => {
        try {
            const res = await fetch(`${baseUrl}/${endpoint.signup}`, {
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
            dispatch({ username: username });
        } catch (e) {
            dispatch(undefined);
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
            {state.userInfo === undefined ? <p>Sign up failed.</p> : <></>}
        </form>
    );
};

export default Signup;
