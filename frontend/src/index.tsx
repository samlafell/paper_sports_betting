// Ensure this file replaces the default render in your project

import React from 'react';
import ReactDOM from 'react-dom/client';
import AppRoutes from '../app/routes'; // Correct relative path

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>
    <AppRoutes />
    </React.StrictMode>
);