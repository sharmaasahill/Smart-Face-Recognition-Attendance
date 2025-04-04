import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Container, Typography, Paper, TextField, IconButton, InputAdornment } from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { motion } from "framer-motion";
import axios from "axios";

const Login = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [otp, setOtp] = useState("");
    const [error, setError] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [otpSent, setOtpSent] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleLogin = async () => {
        if (!username || !password) {
            setError("Please enter both username and password!");
            return;
        }

        if (username === "admin" && password === "admin123") {
            setLoading(true);
            try {
                const response = await axios.post("http://localhost:5000/api/generate-otp", { username });
                if (response.data.message) {
                    setOtpSent(true);
                    setError("");
                } else {
                    setError("Failed to send OTP. Try again!");
                }
            } catch (err) {
                setError("Error sending OTP. Check server logs.");
            } finally {
                setLoading(false);
            }
        } else {
            setError("Invalid username or password!");
        }
    };

    const handleVerifyOtp = async () => {
        if (!otp) {
            setError("Please enter the OTP!");
            return;
        }

        setLoading(true);
        try {
            const response = await axios.post("http://localhost:5000/api/verify-otp", { username, otp });
            if (response.data.message) {
                navigate("/dashboard");
            } else {
                setError("Invalid OTP! Please try again.");
            }
        } catch (err) {
            setError("Error verifying OTP.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container
            maxWidth={false}
            sx={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                minHeight: "100vh",
                width: "100%",
                background: "linear-gradient(135deg, #0f0c29, #302b63, #24243e)",
                fontFamily: "'Poppins', sans-serif",
                padding: "20px",
            }}
        >
            <motion.div
                initial={{ opacity: 0, y: -50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                style={{ width: "100%", maxWidth: "450px" }}
            >
                <Paper
                    elevation={10}
                    sx={{
                        padding: "40px",
                        textAlign: "center",
                        borderRadius: "12px",
                        backdropFilter: "blur(15px)",
                        backgroundColor: "rgba(255, 255, 255, 0.05)",
                        color: "#fff",
                        width: "100%",
                        border: "1px solid rgba(255, 255, 255, 0.2)",
                        boxShadow: "0px 10px 30px rgba(0, 0, 0, 0.4)",
                    }}
                >
                    <Typography variant="h4" fontWeight="600" gutterBottom sx={{ color: "#ffffff" }}>
                        Admin Login
                    </Typography>

                    <TextField
                        label="Username"
                        variant="outlined"
                        fullWidth
                        margin="normal"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        InputProps={{
                            sx: { color: "#fff", background: "rgba(255, 255, 255, 0.1)", borderRadius: "8px" },
                        }}
                        InputLabelProps={{ sx: { color: "#ccc" } }}
                        disabled={otpSent}
                    />

                    <TextField
                        label="Password"
                        variant="outlined"
                        fullWidth
                        margin="normal"
                        type={showPassword ? "text" : "password"}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        InputProps={{
                            sx: { color: "#fff", background: "rgba(255, 255, 255, 0.1)", borderRadius: "8px" },
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton
                                        onClick={() => setShowPassword(!showPassword)}
                                        edge="end"
                                        sx={{ color: "#fff" }}
                                    >
                                        {showPassword ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                </InputAdornment>
                            ),
                        }}
                        InputLabelProps={{ sx: { color: "#ccc" } }}
                        disabled={otpSent}
                    />

                    {otpSent && (
                        <TextField
                            label="Enter OTP"
                            variant="outlined"
                            fullWidth
                            margin="normal"
                            value={otp}
                            onChange={(e) => setOtp(e.target.value)}
                            InputProps={{
                                sx: { color: "#fff", background: "rgba(255, 255, 255, 0.1)", borderRadius: "8px" },
                            }}
                            InputLabelProps={{ sx: { color: "#ccc" } }}
                        />
                    )}

                    {error && (
                        <Typography color="error" sx={{ marginTop: "10px", fontSize: "14px" }}>
                            {error}
                        </Typography>
                    )}

                    <motion.div
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        transition={{ duration: 0.2 }}
                        style={{ width: "100%" }}
                    >
                        {!otpSent ? (
                            <Button
                                variant="contained"
                                fullWidth
                                onClick={handleLogin}
                                disabled={loading}
                                sx={{
                                    marginTop: "20px",
                                    padding: "12px",
                                    fontSize: "16px",
                                    fontWeight: "bold",
                                    background: "linear-gradient(135deg, #6a11cb, #2575fc)",
                                    color: "#fff",
                                    borderRadius: "8px",
                                    boxShadow: "0px 4px 15px rgba(0, 123, 255, 0.4)",
                                    transition: "0.3s",
                                    "&:hover": {
                                        background: "linear-gradient(135deg, #2575fc, #6a11cb)",
                                        boxShadow: "0px 6px 20px rgba(0, 123, 255, 0.6)",
                                    },
                                }}
                            >
                                {loading ? "Sending OTP..." : "Login"}
                            </Button>
                        ) : (
                            <Button
                                variant="contained"
                                fullWidth
                                onClick={handleVerifyOtp}
                                disabled={loading}
                                sx={{
                                    marginTop: "20px",
                                    padding: "12px",
                                    fontSize: "16px",
                                    fontWeight: "bold",
                                    background: "linear-gradient(135deg, #ff512f, #dd2476)",
                                    color: "#fff",
                                    borderRadius: "8px",
                                    boxShadow: "0px 4px 15px rgba(255, 0, 0, 0.4)",
                                    transition: "0.3s",
                                    "&:hover": {
                                        background: "linear-gradient(135deg, #dd2476, #ff512f)",
                                        boxShadow: "0px 6px 20px rgba(255, 0, 0, 0.6)",
                                    },
                                }}
                            >
                                {loading ? "Verifying OTP..." : "Verify OTP"}
                            </Button>
                        )}
                    </motion.div>
                </Paper>
            </motion.div>
        </Container>
    );
};

export default Login;
