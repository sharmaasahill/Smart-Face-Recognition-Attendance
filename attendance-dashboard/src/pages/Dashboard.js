import React, { useEffect, useState } from "react";
import axios from "axios";
import {
    Container, Typography, Table, TableBody, TableCell, TableContainer,
    TableHead, TableRow, Paper, Button, Box, Select, MenuItem, TextField
} from "@mui/material";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import LogoutIcon from '@mui/icons-material/Logout';
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';

// Embedded RegisterUser Component
const RegisterUser = () => {
    const [name, setName] = useState("");
    const [status, setStatus] = useState("");

    const handleRegister = async () => {
        if (!name.trim()) {
            setStatus("Name is required.");
            return;
        }

        setStatus("Registering...");

        try {
            const response = await axios.post("http://localhost:5000/register", {
                name,
            });

            if (response.data.success) {
                setStatus(response.data.message);
                setName("");
            } else {
                setStatus("Failed to register user.");
            }
        } catch (error) {
            setStatus("Error during registration.");
            console.error(error);
        }
    };

    return (
        <Box sx={{
            mt: 4,
            mb: 2,
            width: "100%",
            maxWidth: "600px",
            backgroundColor: "#fff",
            padding: 3,
            borderRadius: 2,
            boxShadow: 3
        }}>
            <Typography variant="h6" gutterBottom>Register New User</Typography>
            <TextField
                fullWidth
                label="Full Name"
                variant="outlined"
                value={name}
                onChange={(e) => setName(e.target.value)}
                sx={{ mb: 2 }}
            />
            <Button variant="contained" onClick={handleRegister}>
                Register
            </Button>
            {status && (
                <Typography sx={{ mt: 2, fontSize: "0.9rem", color: "#666" }}>
                    {status}
                </Typography>
            )}
        </Box>
    );
};

const Dashboard = () => {
    const [attendance, setAttendance] = useState([]);
    const [filteredAttendance, setFilteredAttendance] = useState([]);
    const [darkMode, setDarkMode] = useState(true);
    const [selectedDate, setSelectedDate] = useState("");
    const [availableDates, setAvailableDates] = useState([]);
    const [chartData, setChartData] = useState([]);

    const fetchAttendance = () => {
        axios.get("http://127.0.0.1:5000/api/attendance")
            .then((response) => {
                const data = response.data || [];
                setAttendance(data);
                extractUniqueDates(data);
                filterByDate(data, selectedDate);
                prepareChartData(data);
            })
            .catch((error) => console.error("Error fetching attendance data:", error));
    };

    const extractUniqueDates = (data) => {
        const uniqueDates = [...new Set(data.map(entry => entry.date))];
        setAvailableDates(uniqueDates);
        if (!selectedDate && uniqueDates.length > 0) {
            setSelectedDate(uniqueDates[0]);
        }
    };

    const filterByDate = (data, date) => {
        const filteredData = date ? data.filter(entry => entry.date === date) : data;
        setFilteredAttendance(filteredData);
    };

    const prepareChartData = (data) => {
        const dateMap = {};
        data.forEach(entry => {
            dateMap[entry.date] = (dateMap[entry.date] || 0) + 1;
        });
        const formattedData = Object.entries(dateMap).map(([date, count]) => ({ date, count }));
        setChartData(formattedData);
    };

    useEffect(() => {
        fetchAttendance();
        const interval = setInterval(fetchAttendance, 5000);
        return () => clearInterval(interval);
    }, [selectedDate]);

    return (
        <Container
            maxWidth={false}
            sx={{
                minHeight: "100vh",
                width: "100%",
                background: darkMode ? "#111" : "#f5f5f5",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                padding: "20px",
                transition: "0.4s",
                fontFamily: "'Poppins', sans-serif",
            }}
        >
            {/* Header */}
            <Box sx={{
                display: "flex",
                justifyContent: "space-between",
                width: "100%",
                maxWidth: "1200px",
                alignItems: "center",
                mb: 2
            }}>
                <Typography variant="h4" fontWeight="600" sx={{ color: darkMode ? "#fff" : "#333" }}>
                    Attendance Dashboard
                </Typography>
                <Box>
                    <Button onClick={() => setDarkMode(!darkMode)} sx={{ mx: 1 }}>
                        {darkMode ? <LightModeIcon sx={{ color: "#fff" }} /> : <DarkModeIcon sx={{ color: "#333" }} />}
                    </Button>
                    <Button
                        variant="contained"
                        onClick={() => (window.location.href = "/")}
                        sx={{
                            background: "linear-gradient(135deg, #6a11cb, #2575fc)",
                            color: "#fff",
                            borderRadius: "8px",
                            "&:hover": { background: "linear-gradient(135deg, #2575fc, #6a11cb)" },
                        }}
                    >
                        <LogoutIcon sx={{ mr: 1 }} /> Logout
                    </Button>
                </Box>
            </Box>

            {/* Register Form */}
            <RegisterUser />

            {/* Date Selector */}
            <Box sx={{ width: "100%", maxWidth: "1200px", mb: 3, textAlign: "center" }}>
                <Typography variant="h6" sx={{ color: darkMode ? "#bbb" : "#333", mb: 1 }}>
                    Select Date
                </Typography>
                <Select
                    value={selectedDate}
                    onChange={(e) => {
                        setSelectedDate(e.target.value);
                        filterByDate(attendance, e.target.value);
                    }}
                    sx={{
                        backgroundColor: darkMode ? "#222" : "#fff",
                        color: darkMode ? "#fff" : "#333",
                        width: "200px",
                    }}
                >
                    {availableDates && availableDates.length > 0 ? (
                        availableDates.map((date, index) => (
                            <MenuItem key={index} value={date}>
                                {date}
                            </MenuItem>
                        ))
                    ) : (
                        <MenuItem value="">No Data</MenuItem>
                    )}
                </Select>
            </Box>

            {/* Attendance Table */}
            <TableContainer
                component={Paper}
                sx={{
                    width: "100%",
                    maxWidth: "1200px",
                    backgroundColor: darkMode ? "#222" : "#fff",
                    borderRadius: "12px",
                    overflow: "hidden",
                }}
            >
                <Table>
                    <TableHead>
                        <TableRow sx={{ background: "linear-gradient(135deg, #6a11cb, #2575fc)" }}>
                            <TableCell sx={{ color: "#fff", fontWeight: "bold" }}>ID</TableCell>
                            <TableCell sx={{ color: "#fff", fontWeight: "bold" }}>Name</TableCell>
                            <TableCell sx={{ color: "#fff", fontWeight: "bold" }}>Date</TableCell>
                            <TableCell sx={{ color: "#fff", fontWeight: "bold" }}>Time</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {filteredAttendance.map((entry) => (
                            <TableRow key={entry.id} sx={{ backgroundColor: darkMode ? "#333" : "#fff" }}>
                                <TableCell sx={{ color: darkMode ? "#fff" : "#333" }}>{entry.id}</TableCell>
                                <TableCell sx={{ color: darkMode ? "#fff" : "#333" }}>{entry.name}</TableCell>
                                <TableCell sx={{ color: darkMode ? "#fff" : "#333" }}>{entry.date}</TableCell>
                                <TableCell sx={{ color: darkMode ? "#fff" : "#333" }}>{entry.time}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Attendance Trend Chart */}
            <Typography variant="h6" sx={{ color: darkMode ? "#bbb" : "#333", mt: 4 }}>Attendance Trends</Typography>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                    <XAxis dataKey="date" stroke={darkMode ? "#fff" : "#333"} />
                    <YAxis stroke={darkMode ? "#fff" : "#333"} />
                    <CartesianGrid stroke={darkMode ? "#444" : "#ddd"} />
                    <Tooltip />
                    <Line type="monotone" dataKey="count" stroke="#6a11cb" strokeWidth={2} />
                </LineChart>
            </ResponsiveContainer>
        </Container>
    );
};

export default Dashboard;
