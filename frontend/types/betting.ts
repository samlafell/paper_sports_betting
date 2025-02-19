export interface Bet {
  id: string;
  userId: string;
  market: string;
  outcome: string;
  odds: number;
  stake: number;
  status: 'pending' | 'won' | 'lost';
}

export interface Market {
    id: string;
    name: string;
    outcomes: Outcome[];
}

export interface Outcome {
    id: string;
    name: string;
    odds: number;
}

export interface OddsUpdate {
  eventId: string;
  odds: number;
  // Add additional properties based on your odds update structure
}

// Add other relevant types 