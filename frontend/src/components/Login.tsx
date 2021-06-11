import React, { useContext, useState } from "react";
import { useHistory } from "react-router-dom";
import { AuthContext } from "../context/context";
import { login } from "../api";
import { Flex, Text } from "@chakra-ui/layout";
import { Input } from "@chakra-ui/input";
import { Button } from "@chakra-ui/button";
import { FormLabel } from "@chakra-ui/form-control";
import Header from "./Header";
import { validateForm } from "../validate";

const Login: React.FC = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [logInError, setLogInError] = useState<string | undefined>(undefined);
    const { dispatch } = useContext(AuthContext);
    let history = useHistory();

    const submit = async () => {
        try {
            await login(username, password);
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
            setLogInError("Username or password is wrong. Please try again.");
        }
    };

    return (
        <>
            <Header />
            <Flex direction="column" mt="10" px="30%">
                <form>
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
                    {logInError ? (
                        <Text mb="4" px="3" color="red.500">
                            {logInError}
                        </Text>
                    ) : (
                        <></>
                    )}
                    <Button
                        colorScheme="blue"
                        width="100%"
                        onClick={e => {
                            e.preventDefault();
                            const error = validateForm(username, password);
                            if (error) {
                                setLogInError(error);
                                return;
                            }
                            submit();
                        }}
                    >
                        Log in
                    </Button>
                </form>
            </Flex>
        </>
    );
};

export default Login;
