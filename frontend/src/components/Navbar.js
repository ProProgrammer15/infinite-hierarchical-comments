import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate
import { logout } from '../redux/slices/authSlice';

const Navbar = () => {
    const { user, isLoggedIn } = useSelector((state) => state.auth);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleLogout = () => {
        dispatch(logout());
        navigate('/login');
    };

    console.log("USER: ", user)

    return (
        <AppBar position="static" sx={{ backgroundColor: '#1976d2' }}>
            <Toolbar>
                {/* App Title */}
                <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
                    Tree Comments
                </Typography>

                {/* Links */}
                <Box sx={{ display: 'flex', gap: 2 }}>
                    <Button color="inherit" component={Link} to="/" sx={{ fontSize: '1rem' }}>
                        Comments
                    </Button>
                    {!isLoggedIn && (
                        <>
                            <Button color="inherit" component={Link} to="/login" sx={{ fontSize: '1rem' }}>
                                Login
                            </Button>
                            <Button color="inherit" component={Link} to="/register" sx={{ fontSize: '1rem' }}>
                                Register
                            </Button>
                        </>
                    )}
                </Box>

                {/* User Info and Logout */}
                {isLoggedIn && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, ml: 4 }}>
                        <Typography variant="body1" sx={{ fontSize: '0.9rem', fontStyle: 'italic' }}>
                            Welcome, <strong>{user?.username}</strong>
                        </Typography>
                        <Button
                            color="secondary"
                            variant="outlined"
                            size="small"
                            onClick={handleLogout}
                            sx={{
                                borderColor: 'white',
                                color: 'white',
                                '&:hover': {
                                    borderColor: '#ccc',
                                    backgroundColor: '#1565c0',
                                },
                            }}
                        >
                            Logout
                        </Button>
                    </Box>
                )}
            </Toolbar>
        </AppBar>
    );
};

export default Navbar;
