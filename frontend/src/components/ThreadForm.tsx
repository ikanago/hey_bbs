import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/context";
import { HStack } from "@chakra-ui/layout";
import { Input } from "@chakra-ui/input";
import { Button } from "@chakra-ui/button";
import { createThread } from "../api";
import type { Thread } from "./ThreadContainer";

type Props = {
    setThreads: React.Dispatch<React.SetStateAction<Thread[]>>;
};

const TopThreads: React.FC<Props> = props => {
    const [threadName, setThreadName] = useState("");

    const handleClick = async () => {
        try {
            const json = await createThread(threadName);
            props.setThreads(json);
        } catch (e) {
            console.error(e);
            props.setThreads([]);
        } finally {
            setThreadName("");
        }
    };

    return (
        <HStack>
            <Input
                placeholder="Let's create your thread!"
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
                Create thread
            </Button>
        </HStack>
    );
};

export default TopThreads;
