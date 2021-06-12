import React from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import { Box, ChakraProvider, extendTheme } from "@chakra-ui/react";
import AuthProvider from "./context/AuthProvider";
import Login from "./components/Login";
import PostContainer from "./components/PostContainer";
import PrivateRoute from "./components/PrivateRoute";
import Signup from "./components/Signup";
import ThreadContainer from "./components/ThreadContainer";

const theme = extendTheme({
    styles: {
        global: {
            "html, body": {
                color: "#CCCCCC",
                backgroundColor: "#1A202C",
            },
        },
    },
    colors: {
        brand: {
            100: "#CCCCCC",
            700: "#394660",
            800: "#273042",
            900: "#1A202C",
        },
    },
});

const App: React.FC = () => {
    return (
        <ChakraProvider theme={theme}>
            <AuthProvider>
                <Box px="20%">
                    <BrowserRouter>
                        <Switch>
                            <PrivateRoute path="/threads" fallback="/login">
                                <ThreadContainer />
                            </PrivateRoute>
                            <PrivateRoute path="/posts/:threadName" fallback="/login">
                                <PostContainer />
                            </PrivateRoute>
                            <Route path="/signup" children={<Signup />} />
                            <Route path="/login" children={<Login />} />
                        </Switch>
                    </BrowserRouter>
                </Box>
            </AuthProvider>
        </ChakraProvider>
    );
};

export default App;
