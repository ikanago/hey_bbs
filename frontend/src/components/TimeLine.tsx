import React from "react";
import PostCard from "./Post";
import { Post } from "./PostForm";

type Props = {
    posts: Post[];
};

const TimeLine: React.FC<Props> = props => {
    return (
        <ul>
            {props.posts.map(post => (
                <PostCard key={post.id} text={post.text} username={post.username} />
            ))}
        </ul>
    );
};

export default TimeLine;
