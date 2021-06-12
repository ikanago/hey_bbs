import { baseUrl, endpoint } from "./const";

export const verifyLogin = async () => {
    const res = await fetch(`${baseUrl}/${endpoint.verifyLogin}`, {
        method: "GET",
        credentials: "include",
    });
    if (!res.ok) {
        return {};
    }
    return await res.json();
};

export const signup = async (username: string, password: string) => {
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

export const login = async (username: string, password: string) => {
    const res = await fetch(`${baseUrl}/${endpoint.login}`, {
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

export const logout = async () => {
    await fetch(`${baseUrl}/${endpoint.logout}`, {
        method: "GET",
        credentials: "include",
    });
};

export const getPosts = async (thread_name: string): Promise<any> => {
    const res = await fetch(`${baseUrl}/${endpoint.posts}/${thread_name}`, {
        method: "GET",
        credentials: "include",
    });
    if (!res.ok) {
        throw new Error(`HTTP error: ${res.status}`);
    }
    return await res.json();
};

export const createPost = async (text: string, threadName: string): Promise<any> => {
    const res = await fetch(`${baseUrl}/${endpoint.posts}/${threadName}`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            text: text,
        }),
    });
    if (!res.ok) {
        throw new Error(`HTTP error: ${res.status}`);
    }
    return await res.json();
};

export const getThreads = async (): Promise<any> => {
    const res = await fetch(`${baseUrl}/${endpoint.threads}`, {
        method: "GET",
        credentials: "include",
    });
    if (!res.ok) {
        throw new Error(`HTTP error: ${res.status}`);
    }
    return await res.json();
};

export const createThread = async (threadName: string): Promise<any> => {
    const res = await fetch(`${baseUrl}/${endpoint.threads}`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            thread_name: threadName,
        }),
    });
    if (!res.ok) {
        throw new Error(`HTTP error: ${res.status}`);
    }
    return await res.json();
};
