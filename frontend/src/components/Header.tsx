import { Button, ButtonGroup } from "@chakra-ui/button";
import { Flex, Spacer, Text } from "@chakra-ui/layout";
import React from "react";
import { User } from "../context/context";

type Props = {
    user?: User;
};

const Header: React.FC<Props> = props => {
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
                    <Button variant="outline">Log out</Button>
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
