import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/context";
import { getThreads } from "../api";
import ThreadForm from "./ThreadForm";
import Header from "./Header";
import ThreadCard from "./ThreadCard";

export type Thread = {
    thread_id: string;
    thread_name: string;
};

const TopThreads: React.FC = () => {
    const [threads, setThreads] = useState<Thread[]>([]);
    const { state } = useContext(AuthContext);

    useEffect(() => {
        (async () => {
            try {
                const json = await getThreads();
                setThreads(json);
            } catch (e) {
                console.error(e);
                setThreads([]);
            }
        })();
    }, []);

    return (
        <>
            <Header user={state.user} />
            <ThreadForm setThreads={setThreads} />
            {threads.map(thread => (
                <ThreadCard
                    key={thread.thread_id}
                    thread_name={thread.thread_name}
                />
            ))}
        </>
    );
};

export default TopThreads;
