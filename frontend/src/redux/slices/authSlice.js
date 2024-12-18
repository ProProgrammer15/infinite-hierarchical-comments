import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { signup, login } from '../../api/authApi';

const getToken = () => {
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    return refreshToken || accessToken;
};

const getUserFromStorage = () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
};

export const signupUser = createAsyncThunk('auth/signupUser', async (payload, { rejectWithValue }) => {
    try {
        const response = await signup(payload);
        return response;
    } catch (error) {
        return rejectWithValue(error.response?.data?.message || 'Signup failed');
    }
});

export const loginUser = createAsyncThunk('auth/loginUser', async (payload, { rejectWithValue }) => {
    try {
        const response = await login(payload);
        const { access_token, refresh_token, user } = response;

        // Store tokens and user based on "remember me"
        if (payload.remember_me) {
            localStorage.setItem('refresh_token', refresh_token);
        } else {
            localStorage.setItem('access_token', access_token);
        }

        localStorage.setItem('user', JSON.stringify(user));
        return user;
    } catch (error) {
        return rejectWithValue(error.response?.data?.message || 'Login failed');
    }
});

const initialState = {
    user: getUserFromStorage(),
    isLoggedIn: !!getToken(),
    loading: false,
    error: null,
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        logout(state) {
            state.user = null;
            state.isLoggedIn = false;
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(signupUser.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(signupUser.fulfilled, (state, action) => {
                state.loading = false;
                state.user = action.payload;
                state.isLoggedIn = true;
            })
            .addCase(signupUser.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })
            .addCase(loginUser.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(loginUser.fulfilled, (state, action) => {
                state.loading = false;
                state.user = action.payload;
                state.isLoggedIn = true;
            })
            .addCase(loginUser.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            });
    },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
