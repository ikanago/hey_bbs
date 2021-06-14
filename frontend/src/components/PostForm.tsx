import React, { useRef, useState } from "react";
import { createPost, uploadImage } from "../api";
import { Button, Flex, Textarea } from "@chakra-ui/react";
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
    const fileUploadRef = useRef<HTMLInputElement | null>(null);

    const handleClick = async () => {
        try {
            let image_id: string | undefined;
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
                mb="3"
            />
            <Flex direction="row" alignItems="flex-end" mb="3">
                <Button
                    mr="3"
                    fontSize="20"
                    colorScheme="green"
                    onClick={_ => {
                        fileUploadRef.current?.click();
                    }}
                >
                    Image
                </Button>
                <Button
                    mr="3"
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
                    hidden
                    type="file"
                    ref={fileUploadRef}
                    accept={acceptMimeType}
                    onChange={handleChange}
                />
            </Flex>
            {file ? <img src={URL.createObjectURL(file)} height="150%" /> : <></>}
        </>
    );
};

export default PostForm;
