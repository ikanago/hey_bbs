import React from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import "./App.css";
import PostForm from "./components/PostForm";
import Signup from "./components/Signup";

const App: React.FC = () => {
    return (
        <BrowserRouter>
            <Switch>
                <Route path="/posts" children={<PostForm />} />
                <Route path="/signup" children={<Signup />} />
            </Switch>
        </BrowserRouter>
    );
};

export default App;
