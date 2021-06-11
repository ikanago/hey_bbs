import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/context";
import { HStack } from "@chakra-ui/layout";
import { Input } from "@chakra-ui/input";
import { Button } from "@chakra-ui/button";
import { getThreads, createThread } from "../api";
import Header from "./Header";
import ThreadCard from "./ThreadCard";

export type Threads = {
    thread_id: string;
    thread_name: string;
};

const TopThreads: React.FC = () => {
    const [threadName, setThreadName] = useState("");
    const [threads, setThreads] = useState<Threads[]>([]);
    const { state } = useContext(AuthContext);

    useEffect(() => {
        (async () => {
            try {
                console.log(state);
                const json = await getThreads();
                console.log(state);
                setThreads(json);
            } catch (e) {
                console.error(e);
                setThreads([]);
            }
        })();
    }, []);

    const handleClick = async () => {
        try {
            const json = await createThread(threadName);
            setThreads(json);
        } catch (e) {
            console.error(e);
            setThreads([]);
        } finally {
            setThreadName("");
        }
    }

    return (
        <>
            <Header user={state.user} />
            <HStack>
                <Input
                    placeholder="What's going on?"
                    onChange={event => setThreadName(event.target.value)}
                    value={threadName}
                    type="text"
                />
                <Button
                    colorScheme="blue"
                    onClick={e => {
                        e.preventDefault();
                        handleClick();
                    }}
                >
                    Send
                </Button>
            </HStack>
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
