import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/context";
import { createPost, getPosts } from "../api";
import TimeLine from "./TimeLine";
import Header from "./Header";
import { Box, HStack } from "@chakra-ui/layout";
import { Input } from "@chakra-ui/input";
import { Button } from "@chakra-ui/button";

export type Post = {
    id: number;
    text: string;
    username: string;
};

const PostForm: React.FC = () => {
    const [posts, setPosts] = useState<Post[]>([]);
    const [text, setText] = useState("");
    const { state } = useContext(AuthContext);

    useEffect(() => {
        (async () => {
            try {
                const json = await getPosts();
                setPosts(json);
            } catch (e) {
                console.error(e);
                setPosts([]);
            }
        })();
    }, []);

    const handleClick = async () => {
        try {
            const json = await createPost(text);
            setPosts(json);
        } catch (e) {
            console.error(e);
            setPosts([]);
        } finally {
            setText("");
        }
    };

    return (
        <>
            <Header user={state.user} />
            <HStack>
                <Input
                    placeholder="What's going on?"
                    onChange={event => setText(event.target.value)}
                    value={text}
                    type="text"
                />
                <Button colorScheme="blue" onClick={handleClick}>
                    Send
                </Button>
            </HStack>
            <TimeLine posts={posts} />
        </>
    );
};

export default PostForm;
