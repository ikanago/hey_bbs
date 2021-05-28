import React, { useEffect, useState } from "react";
import TimeLine from "./TimeLine";

export type Post = {
    id: number;
    text: string
};

const PostForm: React.FC = () => {
    const [posts, setPosts] = useState<Post[]>([]);
    const [text, setText] = useState("");

    const url = "http://localhost:8080/posts";
    const params = {
        "text": text,
    };
    const makeRequest = () => {
        console.log("Sending");
        fetch(url, {
            "method": "POST",
            "mode": "cors",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": JSON.stringify(params),
        })
        .then(res => {
            if (res.status >= 400) {
                throw new Error();
            }
            setText("");
            return res.json();
        })
        .then(json => {
            setPosts(json);
        })
        .catch(err => {
            console.error(err);
            setPosts([]);
        });
    };

    return (
        <>
            <TimeLine posts={posts}/>
            <input onChange={event => setText(event.target.value)} value={text} type="text" />
            <button onClick={makeRequest}>Send</button>
        </>
    );
}

export default PostForm;
