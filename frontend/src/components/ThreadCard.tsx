import { Box } from "@chakra-ui/layout";
import React from "react";
import type { Thread } from "./ThreadContainer";

const ThreadCard: React.FC<Partial<Thread>> = props => {
    return (
        <Box mt={3} textAlign="left" bg="brand.800" borderRadius="lg">
            <Box pl={5} fontSize="28">
                {props.thread_name}
            </Box>
        </Box>
    );
};

export default ThreadCard;
