import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/context";
import TimeLine from "./TimeLine";
import { createPost, getPosts } from "../api";
import { Box } from "@chakra-ui/layout";

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
        <Box px={40}>
            <div>{state.user?.username}</div>
            <TimeLine posts={posts} />
            <input
                onChange={event => setText(event.target.value)}
                value={text}
                type="text"
            />
            <button onClick={handleClick}>Send</button>
        </Box>
    );
};

export default PostForm;
