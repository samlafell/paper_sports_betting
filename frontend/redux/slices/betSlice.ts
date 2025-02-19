import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Bet } from '../../types/betting';

interface BetState {
  bets: Bet[];
  // Add other bet-related state (e.g., current selections)
}

const initialState: BetState = {
  bets: [],
};

const betSlice = createSlice({
  name: 'bets',
  initialState,
  reducers: {
    addBet: (state, action: PayloadAction<Bet>) => {
      state.bets.push(action.payload);
    },
    updateBetStatus: (state, action: PayloadAction<{ betId: string; status: 'won' | 'lost' }>) => {
        const { betId, status } = action.payload;
        const bet = state.bets.find((b) => b.id === betId);
        if (bet) {
            bet.status = status;
        }
    }
    // Add other reducers (e.g., removeBet, updateOdds, etc.)
  },
});

export const { addBet, updateBetStatus } = betSlice.actions;
export default betSlice.reducer; 