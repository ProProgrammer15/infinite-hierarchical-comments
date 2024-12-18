import React, { useState, useEffect } from 'react';
import { Container, Typography, Paper, TextField, Button, CircularProgress, Alert } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { fetchComments, createComment, deleteComment } from '../redux/slices/commentsSlice';
import { useNavigate } from 'react-router-dom';

const Comments = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { comments, loading, error } = useSelector((state) => state.comments);
    const { user } = useSelector((state) => state.auth);

    const [commentText, setCommentText] = useState('');
    const [replyTexts, setReplyTexts] = useState({});
    const [activeReplyId, setActiveReplyId] = useState(null);

    const userId = user?.id || user?.user?.id;

    useEffect(() => {
        dispatch(fetchComments());
    }, [dispatch]);

    const handlePostComment = (parentId = null) => {
        if (!user || !userId) {
            alert('User not authenticated. Please login first.');
            navigate('/login');
            return;
        }

        const text = parentId ? replyTexts[parentId]?.trim() : commentText.trim();

        if (text.length >= 3 && text.length <= 200) {
            dispatch(createComment({ text, user_id: userId, parent_id: parentId }))
                .unwrap()
                .then(() => {
                    if (parentId) {
                        setReplyTexts({ ...replyTexts, [parentId]: '' });
                        setActiveReplyId(null);
                    } else {
                        setCommentText('');
                    }
                    dispatch(fetchComments());
                })
                .catch((err) => console.error('Error posting comment:', err));
        } else {
            alert('Comment must be between 3 and 200 characters.');
        }
    };

    const handleDeleteComment = (commentId) => {
        if (window.confirm('Are you sure you want to delete this comment?')) {
            dispatch(deleteComment(commentId))
                .then(() => dispatch(fetchComments()))
                .catch((err) => console.error('Error deleting comment:', err));
        }
    };

    const handleReplyChange = (commentId, text) => {
        setReplyTexts({ ...replyTexts, [commentId]: text });
    };

    const renderComments = (commentsList) => (
        <div>
            {commentsList.map((comment) => (
                <Paper key={comment.id} sx={{ p: 2, mb: 1, ml: comment.parent_id ? 4 : 0 }}>
                    <Typography variant="body1">
                        <strong> {comment.username}</strong>
                    </Typography>
                    <Typography>{comment.text}</Typography>

                    {/* Delete Button */}
                    {userId === comment.user_id && (
                        <Button
                            variant="outlined"
                            color="secondary"
                            size="small"
                            onClick={() => handleDeleteComment(comment.id)}
                            sx={{ mt: 1, mr: 1 }}
                        >
                            Delete
                        </Button>
                    )}

                    {/* Reply Button */}
                    <Button
                        variant="text"
                        size="small"
                        onClick={() => setActiveReplyId(comment.id)}
                        sx={{ mt: 1 }}
                    >
                        Reply
                    </Button>

                    {/* Reply Input */}
                    {activeReplyId === comment.id && (
                        <div style={{ marginTop: '10px' }}>
                            <TextField
                                placeholder="Write a reply..."
                                fullWidth
                                multiline
                                value={replyTexts[comment.id] || ''}
                                onChange={(e) => handleReplyChange(comment.id, e.target.value)}
                            />
                            <Button
                                onClick={() => handlePostComment(comment.id)}
                                variant="contained"
                                color="primary"
                                sx={{ mt: 1 }}
                            >
                                Post Reply
                            </Button>
                        </div>
                    )}

                    {/* Render Nested Comments */}
                    {comment.replies && comment.replies.length > 0 && renderComments(comment.replies)}
                </Paper>
            ))}
        </div>
    );

    return (
        <Container>
            <Typography variant="h4">Comments</Typography>

            {loading && <CircularProgress sx={{ mt: 2 }} />}
            {error && <Alert severity="error">{error}</Alert>}

            {/* New Comment Input */}
            <Paper sx={{ p: 2, mb: 2 }}>
                <TextField
                    placeholder="Write a comment..."
                    fullWidth
                    multiline
                    value={commentText}
                    onChange={(e) => setCommentText(e.target.value)}
                />
                <Button onClick={() => handlePostComment(null)} variant="contained" color="primary" sx={{ mt: 1 }}>
                    Post Comment
                </Button>
            </Paper>

            {/* Render Comments */}
            {renderComments(comments)}
        </Container>
    );
};

export default Comments;
