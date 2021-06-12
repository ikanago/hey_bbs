import { Box } from "@chakra-ui/layout";
import { Link } from "@chakra-ui/react";
import React from "react";
import { Link as ReactLink } from "react-router-dom";
import type { Thread } from "./ThreadContainer";

const ThreadCard: React.FC<Partial<Thread>> = props => {
    return (
        <Link
            as={ReactLink}
            to={`/posts/${props.thread_name}`}
            textDecoration="none"
        >
            <Box
                mt={3}
                textAlign="left"
                bg="brand.800"
                borderRadius="lg"
                _hover={{ bg: "brand.700" }}
            >
                <Box pl={5} fontSize="28">
                    {props.thread_name}
                </Box>
            </Box>
        </Link>
    );
};

export default ThreadCard;
