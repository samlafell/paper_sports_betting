import React from 'react';

// Define a specific type for individual selections
interface Selection {
    id: string;
    name: string;
    odds: number;
    // Add additional properties as needed
}

interface BetSlipProps {
    selections: Selection[];
    onPlaceBet: (selections: Selection[]) => void;
}

const BetSlip: React.FC<BetSlipProps> = ({ selections, onPlaceBet }) => {
    return (
        <div className="border p-4 rounded-md">
            <h2 className="text-xl font-bold mb-4">Bet Slip</h2>
            {selections.length === 0 ? (
                <p>No selections yet.</p>
            ) : (
                <>
                    <ul>
                        {selections.map((selection, index) => (
                            <li key={index}>
                                {selection.name} - {selection.odds}
                            </li>
                        ))}
                    </ul>
                    <button onClick={() => onPlaceBet(selections)}>Place Bet</button>
                </>
            )}
        </div>
    );
};

export default BetSlip; 