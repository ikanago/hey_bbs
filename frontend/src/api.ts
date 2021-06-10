import { baseUrl, endpoint } from "./const";

const verifyLogin = async () => {
    const res = await fetch(`${baseUrl}/${endpoint.verifyLogin}`, {
        method: "GET",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
        },
    });
    if (!res.ok) {
        return {};
    }
    return await res.json();
};

const signup = async (username: string, password: string) => {
    const res = await fetch(`${baseUrl}/${endpoint.signup}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    });
    if (!res.ok) {
        throw new Error();
    }
};

const login = async (username: string, password: string) => {
    const res = await fetch(`${baseUrl}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    });
    if (!res.ok) {
        throw new Error();
    }
};

const getPosts = async (): Promise<any> => {
    const res = await fetch(`${baseUrl}/posts`, {
        method: "GET",
        credentials: "include",
    });
    if (res.status >= 400) {
        throw new Error(`HTTP error: ${res.status}`);
    }
    return await res.json();
};

const createPost = async (text: string): Promise<any> => {
    const res = await fetch(`${baseUrl}/posts`, {
        method: "POST",
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
    return await res.json();
};

export { createPost, getPosts, login, signup, verifyLogin };
