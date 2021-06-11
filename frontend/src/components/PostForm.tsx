import React, { useState } from "react";
import { createPost } from "../api";
import { HStack } from "@chakra-ui/layout";
import { Input } from "@chakra-ui/input";
import { Button } from "@chakra-ui/button";
import { validatePost } from "../validate";
import type { Post } from "./PostContainer";
import { useParams } from "react-router-dom";

type Props = {
    setPosts: React.Dispatch<React.SetStateAction<Post[]>>;
};

const PostForm: React.FC<Props> = props => {
    const [text, setText] = useState("");
    const { threadName } = useParams<{ threadName: string;}>();

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
        <HStack>
            <Input
                placeholder="What's going on?"
                onChange={event => setText(event.target.value)}
                value={text}
                type="text"
            />
            <Button
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
        </HStack>
    );
};

export default PostForm;
