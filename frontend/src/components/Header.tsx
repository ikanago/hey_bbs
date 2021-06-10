import { Button, ButtonGroup } from "@chakra-ui/button";
import { Flex, Spacer, Text } from "@chakra-ui/layout";
import React, { useContext } from "react";
import { AuthContext, User } from "../context/context";
import { logout } from "../api";
import { useHistory } from "react-router";

type Props = {
    user?: User;
};

const Header: React.FC<Props> = props => {
    const { dispatch } = useContext(AuthContext);
    let history = useHistory();

    const handleClick = async () => {
        await logout();
        dispatch({
            type: "logout",
        });
        history.push("/login");
    };

    return (
        <Flex
            align="center"
            bg="brand.800"
            p="4"
            mb="3"
            borderBottomRadius="lg"
        >
            <Text fontSize="32">HeyBBS</Text>
            <Spacer />
            {props.user ? (
                <>
                    <Text fontSize="28" mr="3">
                        {props.user.username}
                    </Text>
                    <Button variant="outline" onClick={handleClick}>
                        Log out
                    </Button>
                </>
            ) : (
                <ButtonGroup spacing="3">
                    <Button as="a" href="/login" variant="outline">
                        Log in
                    </Button>
                    <Button as="a" href="/signup" colorScheme="blue">
                        Sign up
                    </Button>
                </ButtonGroup>
            )}
        </Flex>
    );
};

export default Header;
