import React from "react";

export type Props = {
    text: string;
};

const PostCard: React.FC<Props> = props => {
    return <li>{props.text}</li>;
};

export default PostCard;
