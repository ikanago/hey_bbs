import React from "react";
import { Flex } from "@chakra-ui/react";
import PostForm from "./PostForm";

const Posts: React.FC = () => {
    return (
        <Flex direction={"column"}>
            <PostForm></PostForm>
        </Flex>
    )
}

export default Posts;
