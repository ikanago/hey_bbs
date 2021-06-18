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

export const createPost = async (
    text: string,
    imageId: string | undefined,
    threadName: string
): Promise<any> => {
    const res = await fetch(`${baseUrl}/${endpoint.posts}/${threadName}`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            text: text,
            image_id: imageId,
        }),
    });
    if (!res.ok) {
        throw new Error(`HTTP error: ${res.status}`);
    }
    return await res.json();
};

export const getImage = async (imageId: string): Promise<Blob | undefined> => {
    const res = await fetch(`${baseUrl}/${endpoint.image}`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            image_id: imageId,
        }),
    });
    if (!res.ok) {
        throw new Error(`HTTP error: ${res.status}`);
    }
    const contentLength = res.headers.get("Content-Length");
    if (contentLength === "0" || contentLength === null) {
        return undefined;
    }
    return await res.blob();
};

export const uploadImage = async (image: Blob, fileType: string): Promise<any> => {
    const res = await fetch(`${baseUrl}/${endpoint.uploadImage}`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": fileType,
        },
        body: image,
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
