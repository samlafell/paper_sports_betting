import React from 'react';

interface ButtonProps {
    children: React.ReactNode;
    onClick?: () => void;
    className?: string;
    disabled?: boolean;
}
const Button: React.FC<ButtonProps> = ({ children, onClick, className, disabled }) => {
    return (
        <button
            onClick={onClick}
            className={`px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 disabled:bg-gray-400 ${className}`}
            disabled={disabled}
        >
            {children}
        </button>
    )
}

export default Button; 