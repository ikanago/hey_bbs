import React, { useContext, useState } from "react";
import { useHistory } from "react-router-dom";
import { AuthContext } from "../context/context";
import { signup } from "../api"

const Signup: React.FC = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [signUpError, setSignUpError] =
        useState<string | undefined>(undefined);
    const { dispatch } = useContext(AuthContext);
    let history = useHistory();

    const submit = async () => {
        try {
            await signup(username, password);
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
            setSignUpError(
                "そのユーザ名はすでに使用されています．別のユーザ名をお試しください．"
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
                Sign up
            </button>
            {signUpError ? <p>{signUpError}</p> : <></>}
        </form>
    );
};

export default Signup;
