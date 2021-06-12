import { Box } from "@chakra-ui/layout";
import React, { useEffect, useState } from "react";
import { getImage } from "../api";
import type { Post } from "./PostContainer";

const PostCard: React.FC<Partial<Post>> = props => {
    const [imageUrl, setImageUrl] = useState("");

    useEffect(() => {
        (async () => {
            console.log(props.image_id);
            const blob = await getImage(props.image_id!);
            if (blob) {
                const url = URL.createObjectURL(blob);
                setImageUrl(url);
            }
        })();
    }, []);

    return (
        <Box mt={3} textAlign="left" bg="brand.800" borderRadius="lg">
            <Box pl={5} fontSize="28">
                @{props.username}
            </Box>
            <Box px={7} pb={3} fontSize="20" whiteSpace="pre-wrap">
                {props.text}
            </Box>
            <img src={imageUrl} />
        </Box>
    );
};

export default PostCard;
