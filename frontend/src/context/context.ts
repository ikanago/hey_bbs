import React, { createContext } from "react";

type UserInfo = {
    username: string;
};

type State = {
    userInfo?: UserInfo;
};

type Dispatch = (user?: UserInfo) => void;

type Context = {
    state: State;
    dispatch: Dispatch;
};

type AuthAction = {
    type: "login";
    payload: UserInfo;
};

const defaultContext: Context = {
    state: { userInfo: undefined },
    dispatch: () => {},
};

// const authReducer: React.Reducer<AuthContext, AuthAction> = (state: AuthContext, action: AuthAction) => {
//     switch (action.type) {
//         case "login":
//             if (state.userInfo === undefined) {
//                 state.userInfo = action.payload;
//             }
//             return state;
//         default:
//             return state;
//     }
// };

const AuthContext = createContext(defaultContext);
export { AuthContext, defaultContext };
export type { Context as AuthState, UserInfo };
