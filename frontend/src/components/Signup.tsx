import React, { useContext, useState } from "react";
import { Link, useHistory } from "react-router-dom";
import { Flex } from "@chakra-ui/layout";
import { Input } from "@chakra-ui/input";
import { Button } from "@chakra-ui/button";
import { FormLabel } from "@chakra-ui/form-control";
import { signup } from "../api";
import { AuthContext } from "../context/context";
import FormError from "./FormError";
import Header from "./Header";
import { validateForm } from "../validate";

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
            history.push("/threads");
        } catch (e) {
            setSignUpError("The user name is already used. Try another one.");
        }
    };

    return (
        <>
            <Header />
            <Flex direction="column" mt="10" px="30%">
                <form>
                    {signUpError ? <FormError message={signUpError} /> : <></>}
                    <FormLabel>Username</FormLabel>
                    <Input
                        mb="4"
                        onChange={event => setUsername(event.target.value)}
                        value={username}
                        type="text"
                    />
                    <FormLabel>Password</FormLabel>
                    <Input
                        mb="4"
                        onChange={event => setPassword(event.target.value)}
                        value={password}
                        type="password"
                    />
                    <Button
                        colorScheme="blue"
                        width="100%"
                        onClick={e => {
                            e.preventDefault();
                            const error = validateForm(username, password);
                            if (error) {
                                setSignUpError(error);
                                return;
                            }
                            submit();
                        }}
                    >
                        Sign Up
                    </Button>
                    <Link to="/login">Or you have an account?</Link>
                </form>
            </Flex>
        </>
    );
};

export default Signup;
