import React, { useState } from 'react';
import { TextField, Button, Container, Typography, Paper, Box, CircularProgress, Alert } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { signupUser } from '../redux/slices/authSlice';

const Register = () => {
    const dispatch = useDispatch();
    const { loading, error } = useSelector((state) => state.auth);

    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        dispatch(signupUser(formData));
    };

    return (
        <Container maxWidth="sm" sx={{ mt: 5 }}>
            <Paper elevation={3} sx={{ p: 4, borderRadius: '10px' }}>
                <Box textAlign="center" mb={2}>
                    <Typography variant="h4" color="primary" fontWeight="bold">
                        Register
                    </Typography>
                </Box>

                {error && <Alert severity="error">{error}</Alert>}

                <form onSubmit={handleSubmit}>
                    <TextField
                        label="Username"
                        name="username"
                        fullWidth
                        margin="normal"
                        variant="outlined"
                        onChange={handleChange}
                    />

                    <TextField
                        label="Email"
                        name="email"
                        fullWidth
                        margin="normal"
                        variant="outlined"
                        onChange={handleChange}
                    />

                    <TextField
                        label="Password"
                        name="password"
                        type="password"
                        fullWidth
                        margin="normal"
                        variant="outlined"
                        onChange={handleChange}
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
                        {loading ? <CircularProgress size={24} /> : 'Register'}
                    </Button>
                </form>
            </Paper>
        </Container>
    );
};

export default Register;
