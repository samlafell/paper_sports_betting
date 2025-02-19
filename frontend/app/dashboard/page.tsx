'use client'
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Dashboard() {

    const router = useRouter();

    useEffect(() => {
        const checkAuth = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                router.push('/login');
            }
        }
        checkAuth();
    }, [router]);

    return (
        <div>
            <h1>Dashboard</h1>
            <p>Welcome to your dashboard.  You can manage your bets here.</p>
            {/* Add dashboard components (e.g., BetSlip, OddsDisplay) */}
        </div>
    )
} 