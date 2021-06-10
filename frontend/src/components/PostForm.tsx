import React, { useContext, useEffect, useState } from "react";
import { baseUrl } from "../const";
import { AuthContext } from "../context/context";
import TimeLine from "./TimeLine";

export type Post = {
    id: number;
    text: string;
    username: string;
};

const PostForm: React.FC = () => {
    const [posts, setPosts] = useState<Post[]>([]);
    const [text, setText] = useState("");
    const { state } = useContext(AuthContext);
    const url = `${baseUrl}/posts`;

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
        } finally {
            setText("");
        }
    };

    return (
        <>
            <div>{state.user?.username}</div>
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
