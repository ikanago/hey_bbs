import React, { useState } from "react";
import { createPost } from "../api";
import { Flex, HStack } from "@chakra-ui/layout";
import { Textarea } from "@chakra-ui/react";
import { Button } from "@chakra-ui/button";
import { validatePost } from "../validate";
import type { Post } from "./PostContainer";
import { useParams } from "react-router-dom";

type Props = {
    setPosts: React.Dispatch<React.SetStateAction<Post[]>>;
};

const PostForm: React.FC<Props> = props => {
    const [text, setText] = useState("");
    const { threadName } = useParams<{ threadName: string }>();

    const handleClick = async () => {
        try {
            const json = await createPost(text, threadName);
            props.setPosts(json);
        } catch (e) {
            console.error(e);
            // Remove following line and prompt error message.
            props.setPosts([]);
        } finally {
            setText("");
        }
    };

    return (
        <Flex alignItems="flex-end" justifyContent="space-between">
            <Textarea
                placeholder="What's going on?"
                onChange={event => setText(event.target.value)}
                value={text}
                type="text"
                mr="3"
            />
            <Button
                fontSize="20"
                colorScheme="blue"
                onClick={e => {
                    e.preventDefault();
                    const valid = validatePost(text);
                    if (!valid) {
                        return;
                    }
                    handleClick();
                }}
            >
                Send
            </Button>
        </Flex>
    );
};

export default PostForm;
