'use client';
import React from 'react';

export default function AuthLayout({ children }: { children: React.ReactNode }) {
    return (
      <div>
        {/* Common auth layout (header, footer, etc.) */}
        <h1>Authentication Area</h1>
        {children} {/* The register and login pages will be rendered here */}
      </div>
    );
  }