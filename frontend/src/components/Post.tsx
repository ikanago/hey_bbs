import React from "react";

export type Props = {
    text: string;
    username: string;
};

const PostCard: React.FC<Props> = props => {
    return <li>{props.username}: {props.text}</li>;
};

export default PostCard;
