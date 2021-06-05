import React, { useEffect, useState } from "react";
import TimeLine from "./TimeLine";

export type Post = {
    id: number;
    text: string;
};

const PostForm: React.FC = () => {
    const [posts, setPosts] = useState<Post[]>([]);
    const [text, setText] = useState("");
    const url = "http://localhost:8080/posts";

    useEffect(() => {
        (async () => {
            console.log("posts");
            try {
                const res = await fetch(url, {
                    method: "GET",
                    mode: "cors",
                    credentials: "include",
                });
                if (res.status >= 400) {
                    throw new Error(`HTTP error: ${res.status}`);
                }
                const json = await res.json();
                setPosts(json);
            } catch (e) {
                console.error(e);
                setPosts([]);
            }
        })();
    }, []);

    const createPost = async () => {
        try {
            const res = await fetch(url, {
                method: "POST",
                mode: "cors",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    text: text,
                }),
            });
            if (res.status >= 400) {
                throw new Error(`HTTP error: ${res.status}`);
            }
            const json = await res.json();
            setPosts(json);
        } catch (e) {
            console.error(e);
            setPosts([]);
        }
    };

    return (
        <>
            <TimeLine posts={posts} />
            <input
                onChange={event => setText(event.target.value)}
                value={text}
                type="text"
            />
            <button onClick={createPost}>Send</button>
        </>
    );
};

export default PostForm;
