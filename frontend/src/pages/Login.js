import React, { useState } from 'react';
import { TextField, Button, Container, Typography, Paper, Checkbox, FormControlLabel, Box, CircularProgress, Alert } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { loginUser } from '../redux/slices/authSlice';

const Login = () => {
    const dispatch = useDispatch();
    const { loading, error } = useSelector((state) => state.auth);

    const [formData, setFormData] = useState({
        usernameOrEmail: '',
        password: '',
        remember_me: false,
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData({ ...formData, [name]: type === 'checkbox' ? checked : value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const payload = {
            password: formData.password,
            remember_me: formData.remember_me,
        };

        if (formData.usernameOrEmail.includes('@')) {
            payload.email = formData.usernameOrEmail;
        } else {
            payload.username = formData.usernameOrEmail;
        }

        dispatch(loginUser(payload));
    };

    return (
        <Container maxWidth="sm" sx={{ mt: 5 }}>
            <Paper elevation={3} sx={{ p: 4, borderRadius: '10px' }}>
                <Box textAlign="center" mb={2}>
                    <Typography variant="h4" color="primary" fontWeight="bold">
                        Login
                    </Typography>
                </Box>

                {error && <Alert severity="error">{error}</Alert>}

                <form onSubmit={handleSubmit}>
                    <TextField
                        label="Username or Email"
                        name="usernameOrEmail"
                        fullWidth
                        margin="normal"
                        variant="outlined"
                        onChange={handleChange}
                        value={formData.usernameOrEmail}
                    />
                    <TextField
                        label="Password"
                        name="password"
                        type="password"
                        fullWidth
                        margin="normal"
                        variant="outlined"
                        onChange={handleChange}
                        value={formData.password}
                    />
                    <FormControlLabel
                        control={
                            <Checkbox
                                name="remember_me"
                                checked={formData.remember_me}
                                onChange={handleChange}
                            />
                        }
                        label="Remember Me"
                    />
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        fullWidth
                        size="large"
                        sx={{ mt: 2, py: 1 }}
                        disabled={loading}
                    >
                        {loading ? <CircularProgress size={24} /> : 'Login'}
                    </Button>
                </form>
            </Paper>
        </Container>
    );
};

export default Login;
