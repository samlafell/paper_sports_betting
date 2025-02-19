// frontend/app/routes.tsx
// This file is more relevant if you were using react-router-dom.
// With Next.js 13+, routing is file-based, so this file might not be strictly necessary.
//  It's kept here for demonstration, in case you switch to client-side routing.

import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './page';
import Login from './(auth)/login/page';
import Register from './(auth)/register/page';
import Dashboard from './dashboard/page';


const AppRoutes = () => {
    return(
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
        </BrowserRouter>
    )
};

export default AppRoutes; 