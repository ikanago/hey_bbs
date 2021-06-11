import { Box } from "@chakra-ui/layout";
import { Link } from "@chakra-ui/react";
import React from "react";
import { useHistory, Link as ReactLink } from "react-router-dom";
import type { Thread } from "./ThreadContainer";

const ThreadCard: React.FC<Partial<Thread>> = props => {
    return (
        <a
            href={`/posts/${props.thread_name}`}
            style={{ textDecoration: "none" }}
        >
            <Box mt={3} textAlign="left" bg="brand.800" borderRadius="lg">
                <Box pl={5} fontSize="28">
                    {props.thread_name}
                </Box>
            </Box>
        </a>
    );
};

export default ThreadCard;
