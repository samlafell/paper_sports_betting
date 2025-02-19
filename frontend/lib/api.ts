import axios from 'axios';  
import { Bet } from '../types/betting';
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api'; // Or your backend's URL

export const api = axios.create({
  baseURL: API_BASE_URL,
});

// Example: Fetch initial odds data (you might not need this if SSE provides all updates)
export const fetchInitialOdds = async () => {
  try {
    const response = await api.get('/bets/odds'); // Example endpoint
    return response.data;
  } catch (error) {
    console.error("Error fetching initial odds:", error);
    throw error; // Re-throw the error for the calling function to handle
  }
};


// Example: Place a bet (using Axios)
export const placeBet = async (betData: Bet) => {  // Replace 'any' with your bet data type
  try {
    const response = await api.post('/bets', betData); // Example POST endpoint
    return response.data;
  } catch (error) {
    console.error("Error placing bet:", error);
    throw error; // Re-throw for handling by the calling function
  }
};

// ... other API functions (getUser, getSports, etc.) using Axios as needed