import { Box } from "@chakra-ui/layout";
import React from "react";

export type Props = {
    text: string;
    username: string;
};

const PostCard: React.FC<Props> = props => {
    return (
        <Box
            m={3}
            textAlign="left"
            backgroundColor="brand.800"
            borderRadius="lg"
        >
            <Box pl={5} fontSize="28">
                {props.username}
            </Box>
            <Box px={7} pb={3} fontSize="20">
                {props.text}
            </Box>
        </Box>
    );
};

export default PostCard;
