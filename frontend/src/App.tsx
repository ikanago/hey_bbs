import React from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import "./App.css";
import AuthProvider from "./context/AuthProvider";
import Login from "./components/Login";
import PostForm from "./components/PostForm";
import Signup from "./components/Signup";

const App: React.FC = () => {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Switch>
                    <Route path="/posts" children={<PostForm />} />
                    <Route path="/signup" children={<Signup />} />
                    <Route path="/login" children={<Login />} />
                </Switch>
            </BrowserRouter>
        </AuthProvider>
    );
};

export default App;
