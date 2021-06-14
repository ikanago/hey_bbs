import React from "react";
import { Alert, AlertDescription, AlertIcon, Box } from "@chakra-ui/react";

type Props = {
    message: string;
};

const FormError: React.FC<Props> = props => {
    return (
        <Box mb="4">
            <Alert status="error" variant="solid" borderRadius="4">
                <AlertIcon />
                <AlertDescription color="black.800">
                    {props.message}
                </AlertDescription>
            </Alert>
        </Box>
    );
};

export default FormError;
