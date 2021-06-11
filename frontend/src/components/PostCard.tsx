import { Box } from "@chakra-ui/layout";
import React from "react";
import type { Post } from "./PostForm";

const PostCard: React.FC<Partial<Post>> = props => {
    return (
        <Box mt={3} textAlign="left" bg="brand.800" borderRadius="lg">
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
