import React, { createContext } from "react";

type User = {
    username: string;
};

type State = {
    user?: User;
};

type Context = {
    state: State;
    dispatch: React.Dispatch<Action>;
};

type Action = {
    type: "authenticate";
    nextState: State;
};

const authReducer: React.Reducer<State, Action> = (
    state: State,
    action: Action
) => {
    switch (action.type) {
        case "authenticate":
            return action.nextState;
        default:
            return state;
    }
};

const defaultContext: Context = {
    state: { user: undefined },
    dispatch: () => {},
};

const AuthContext = createContext(defaultContext);

export { AuthContext, authReducer };
export type { Context, User };
