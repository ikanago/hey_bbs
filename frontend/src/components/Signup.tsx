import React, { useContext, useState } from "react";
import { Link, useHistory } from "react-router-dom";
import { AuthContext } from "../context/context";
import { signup } from "../api";
import { Flex, Text } from "@chakra-ui/layout";
import { Input } from "@chakra-ui/input";
import { Button } from "@chakra-ui/button";
import { FormLabel } from "@chakra-ui/form-control";

const Signup: React.FC = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [signUpError, setSignUpError] = useState<string | undefined>(undefined);
    const { dispatch } = useContext(AuthContext);
    let history = useHistory();

    const submit = async () => {
        try {
            // await signup(username, password);
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
            setSignUpError("The user name is already used. Try another one.");
        }
    };

    return (
        <Flex direction="column" pt="12" px="40%">
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
                {signUpError ? (
                    <Text mb="4" px="3" color="red.500">
                        {signUpError}
                    </Text>
                ) : (
                    <></>
                )}
                <Button
                    colorScheme="blue"
                    width="100%"
                    onClick={e => {
                        e.preventDefault();
                        submit();
                    }}
                >
                    Sign Up
                </Button>
                <Link to="/login">Or you have an account?</Link>
            </form>
        </Flex>
    );
};

export default Signup;
