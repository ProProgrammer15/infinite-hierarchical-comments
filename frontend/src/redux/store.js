import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import commentsReducer from './slices/commentsSlice';

export const store = configureStore({
    reducer: {
        auth: authReducer,
        comments: commentsReducer,
    },
});
