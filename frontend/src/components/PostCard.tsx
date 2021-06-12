import React, { useEffect, useState } from "react";
import { Box, Center } from "@chakra-ui/react";
import { getImage } from "../api";
import type { Post } from "./PostContainer";

const PostCard: React.FC<Partial<Post>> = props => {
    const [imageUrl, setImageUrl] = useState("");

    useEffect(() => {
        (async () => {
            try {
                if (!props.image_id) {
                    return;
                }
                const blob = await getImage(props.image_id);
                if (blob) {
                    const url = URL.createObjectURL(blob);
                    setImageUrl(url);
                }
            } catch (e) {
                console.error(e);
            }
        })();
    }, []);

    return (
        <Box
            mb={3}
            px={5}
            py={2}
            textAlign="left"
            bg="brand.800"
            borderRadius="lg"
        >
            <Box fontSize="28">@{props.username}</Box>
            <Box px={2} pb={3} fontSize="20" whiteSpace="pre-wrap">
                {props.text}
            </Box>
            {imageUrl.length > 0 ? (
                <Center>
                    <img src={imageUrl} width="50%" />
                </Center>
            ) : (
                <></>
            )}
        </Box>
    );
};

export default PostCard;
