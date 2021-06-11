import { Box } from "@chakra-ui/layout";
import React from "react";
import type { Threads } from "./Threads";

const ThreadCard: React.FC<Partial<Threads>> = props => {
    return (
        <Box mt={3} textAlign="left" bg="brand.800" borderRadius="lg">
            <Box pl={5} fontSize="28">
                {props.thread_name}
            </Box>
        </Box>
    );
};

export default ThreadCard;
