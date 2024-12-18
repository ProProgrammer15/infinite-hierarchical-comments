import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../api/axiosInstance';

// Fetch comments
export const fetchComments = createAsyncThunk('comments/fetchComments', async (_, { rejectWithValue }) => {
    try {
        const response = await axiosInstance.get('/comments/list');
        return response.data.comments;
    } catch (error) {
        return rejectWithValue(error.response?.data?.message || 'Failed to fetch comments');
    }
});

// Add new comment
export const createComment = createAsyncThunk(
    'comments/createComment',
    async ({ text, user_id, parent_id }, { rejectWithValue }) => {
        try {
            const payload = { text, user_id, parent_id };
            const response = await axiosInstance.post('/comments/create', payload);
            return { ...response.data, parent_id };
        } catch (error) {
            return rejectWithValue(error.response?.data?.message || 'Failed to add comment');
        }
    }
);

const addNestedComment = (comments, newComment, parentId) => {
    return comments.map((comment) => {
        if (comment.id === parentId) {
            return {
                ...comment,
                replies: [...comment.replies, { ...newComment, replies: [] }],
            };
        } else if (comment.replies) {
            return {
                ...comment,
                replies: addNestedComment(comment.replies, newComment, parentId),
            };
        }
        return comment;
    });
};

// Delete comment
export const deleteComment = createAsyncThunk(
    'comments/deleteComment',
    async (commentId, { rejectWithValue }) => {
        try {
            await axiosInstance.delete(`/comments/delete/${commentId}`);
            return commentId;
        } catch (error) {
            return rejectWithValue(error.response?.data?.message || 'Failed to delete comment');
        }
    }
);

// Helper function to remove a comment or reply recursively
const removeNestedComment = (comments, commentId) => {
    return comments.filter((comment) => {
        if (comment.id === commentId) return false;
        if (comment.replies) {
            comment.replies = removeNestedComment(comment.replies, commentId);
        }
        return true;
    });
};


const commentsSlice = createSlice({
    name: 'comments',
    initialState: {
        comments: [],
        loading: false,
        error: null,
    },
    reducers: {},
    extraReducers: (builder) => {
        builder
            // Fetch comments
            .addCase(fetchComments.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchComments.fulfilled, (state, action) => {
                state.loading = false;
                state.comments = action.payload;
            })
            .addCase(fetchComments.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
            })

            // Create new comment
            .addCase(createComment.fulfilled, (state, action) => {
                const { parent_id, ...newComment } = action.payload;

                if (!parent_id) {
                    // Top-level comment
                    state.comments = [{ ...newComment, replies: [] }, ...state.comments];
                } else {
                    // Reply to a comment
                    state.comments = addNestedComment(state.comments, newComment, parent_id);
                }
            })
            .addCase(createComment.rejected, (state, action) => {
                state.error = action.payload;
            })
            .addCase(createComment.pending, (state) => {
                state.error = null;
            })

            .addCase(deleteComment.fulfilled, (state, action) => {
                state.comments = removeNestedComment(state.comments, action.payload);
            })
            .addCase(deleteComment.rejected, (state, action) => {
                state.error = action.payload;
            });
    },
});

export default commentsSlice.reducer;
