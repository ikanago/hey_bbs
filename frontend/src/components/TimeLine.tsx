import React from "react";
import PostCard from "./PostCard";
import { Post } from "./PostForm";

type Props = {
    posts: Post[];
};

const TimeLine: React.FC<Props> = props => {
    return (
        <>
            {props.posts.map(post => (
                <PostCard
                    key={post.id}
                    text={post.text}
                    username={post.username}
                />
            ))}
        </>
    );
};

export default TimeLine;
