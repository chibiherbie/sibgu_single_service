import { updateChatAction } from "./actions";

export const updateChatState = {
    chatState: false,
};

export const updateChatReducer = (state, action) => {
    if (action.type === updateChatAction){
        return {
            ...state,
            chatState: action.paygrad,
        };
    }
    else {
        return state;
    }
};
