import React, { useContext } from "react";
import { Redirect, Route } from "react-router-dom";
import { AuthContext } from "../context/context";

type Props = {
    path: string;
    fallback: string;
    children: React.ReactNode;
};

const PrivateRoute: React.FC<Props> = (props: Props) => {
    const { state } = useContext(AuthContext);
    return (
        <Route
            path={props.path}
            render={() =>
                state.user ? props.children : <Redirect to={props.fallback} />
            }
        />
    );
};

export default PrivateRoute;
