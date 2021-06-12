import React, { useState } from "react";
import { createPost, uploadImage } from "../api";
import { Flex, HStack } from "@chakra-ui/layout";
import { Textarea, VStack } from "@chakra-ui/react";
import { Button } from "@chakra-ui/button";
import { validatePost } from "../validate";
import type { Post } from "./PostContainer";
import { useParams } from "react-router-dom";

const acceptFileType = ["jpeg", "png"].map(fileType => `image/${fileType}`);
const acceptMimeType = acceptFileType.join(", ");

type Props = {
    setPosts: React.Dispatch<React.SetStateAction<Post[]>>;
};

const PostForm: React.FC<Props> = props => {
    const [text, setText] = useState("");
    const [file, setFile] = useState<File>();
    const { threadName } = useParams<{ threadName: string }>();

    const handleClick = async () => {
        try {
            let image_id: string | undefined;
            console.log(file?.type);
            if (file && acceptFileType.includes(file.type)) {
                const json = await uploadImage(file);
                image_id = json["image_id"];
            }
            const json = await createPost(text, image_id, threadName);
            props.setPosts(json);
        } catch (e) {
            console.error(e);
            // Remove following line and prompt error message.
            props.setPosts([]);
        } finally {
            setFile(undefined);
            setText("");
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (!files) {
            return;
        }
        const image = files[0];
        setFile(image);
    };

    return (
        <>
            <Textarea
                placeholder="What's going on?"
                onChange={event => setText(event.target.value)}
                value={text}
                type="text"
                mr="3"
            />
            <Flex
                direction="row"
                alignItems="flex-end"
                justifyContent="space-between"
            >
                <VStack>
                    <Button
                        fontSize="20"
                        colorScheme="blue"
                        onClick={e => {
                            e.preventDefault();
                            const valid = validatePost(text);
                            if (!valid) {
                                return;
                            }
                            handleClick();
                        }}
                    >
                        Send
                    </Button>
                    <input
                        type="file"
                        accept={acceptMimeType}
                        onChange={handleChange}
                    />
                </VStack>
                {file ? <img src={URL.createObjectURL(file)} /> : <></>}
            </Flex>
        </>
    );
};

export default PostForm;
