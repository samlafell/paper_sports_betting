import { NextResponse } from 'next/server';
import Redis from 'ioredis';

// Initialize Redis client with better error handling
const redis = new Redis({
    host: 'localhost',
    port: 6379,
    maxRetriesPerRequest: 3,
    retryStrategy(times) {
        const delay = Math.min(times * 50, 2000);
        return delay;
    }
});

redis.on('error', (err) => {
    console.error('Redis connection error:', err);
});

redis.on('connect', () => {
    console.log('Successfully connected to Redis');
});

export async function POST(req: Request) {
    try {
        // Handle preflight OPTIONS request
        if (req.method === 'OPTIONS') {
            return new NextResponse(null, { status: 204 });
        }

        const { username, email, password } = await req.json();

        if (!username || !email || !password) {
            return NextResponse.json(
                { error: 'Username, email, and password are required.' },
                { status: 400 }
            );
        }

        // Wrap Redis operations in a try-catch block
        try {
            const existingUser = await redis.get(`user:${username}`);
            if (existingUser) {
                return NextResponse.json(
                    { error: 'Username already exists.' },
                    { status: 400 }
                );
            }

            // Store user data
            await redis.set(`user:${username}`, JSON.stringify({
                username,
                email,
                password, // Remember to hash passwords in production
                createdAt: new Date().toISOString()
            }));

            // Publish event with timeout
            const publishPromise = redis.publish('new-registrations', JSON.stringify({
                username,
                email,
                timestamp: new Date().toISOString()
            }));

            // Add timeout to publish operation
            const timeout = new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Publish timeout')), 5000)
            );

            await Promise.race([publishPromise, timeout]);

            return NextResponse.json(
                { message: 'Registration successful! Please login.' },
                { status: 201 }
            );
        } catch (redisError) {
            console.error('Redis operation failed:', redisError);
            return NextResponse.json(
                { error: 'Database operation failed.' },
                { status: 500 }
            );
        }
    } catch (error) {
        console.error('Registration error:', error);
        return NextResponse.json(
            { error: 'Internal server error.' },
            { status: 500 }
        );
    }
} 