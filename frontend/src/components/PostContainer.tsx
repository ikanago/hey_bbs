import React, { useContext, useEffect, useState } from "react";
import { Flex } from "@chakra-ui/react";
import { AuthContext } from "../context/context";
import { getPosts } from "../api";
import Header from "./Header";
import PostForm from "./PostForm";
import PostCard from "./PostCard";

export type Post = {
    id: number;
    text: string;
    username: string;
};

const PostContainer: React.FC = () => {
    const [posts, setPosts] = useState<Post[]>([]);
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

    return (
        <Flex direction={"column"}>
            <Header user={state.user} />
            <PostForm setPosts={setPosts}></PostForm>
            {posts.map(post => (
                <PostCard
                    key={post.id}
                    text={post.text}
                    username={post.username}
                />
            ))}
        </Flex>
    );
};

export default PostContainer;
