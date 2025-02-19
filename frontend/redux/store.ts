/*
Store
Purpose
The store is the centralized location that holds the entire state of your application. It serves as the single source of truth, ensuring that every component accesses the same state consistently.


Reducers
Purpose
Reducers are pure functions that determine how the state of the application changes in response to actions sent to the store. They specify the state transitions based on those actions.
*/
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import betReducer from './slices/betSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    bets: betReducer,
    // Add other reducers here
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch; 