import React, { useState } from "react";
import axios from "axios";

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
            } else {
                setStatus("Failed to register user.");
            }
        } catch (error) {
            setStatus("Error during registration.");
            console.error(error);
        }
    };

    return (
        <div className="p-4 rounded-xl shadow-lg bg-white max-w-md mx-auto mt-8">
            <h2 className="text-xl font-semibold mb-2">Register New User</h2>
            <input
                type="text"
                className="border p-2 w-full mb-4 rounded"
                placeholder="Enter full name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <button
                onClick={handleRegister}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
                Register
            </button>
            {status && <p className="mt-4 text-sm text-gray-700">{status}</p>}
        </div>
    );
};

export default RegisterUser;
