import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Define a specific User type with your desired properties
interface User {
  id: string;
  username: string;
  email?: string; // Optional, adjust as needed
  // Add additional properties, such as role, token, etc.
}

interface AuthState {
  user: User | null;  // Use a specific user type (User)
  isAuthenticated: boolean;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginSuccess: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
      state.isAuthenticated = true;
    },
    logout: (state) => {
      state.user = null;
      state.isAuthenticated = false;
    },
  },
});

export const { loginSuccess, logout } = authSlice.actions;
export default authSlice.reducer; 