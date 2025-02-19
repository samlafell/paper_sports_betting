import React from 'react';

interface OddsDisplayProps {
  odds: number; // Or a more complex odds object
  marketName: string;
  outcomeName: string;
}

const OddsDisplay: React.FC<OddsDisplayProps> = ({ odds, marketName, outcomeName }) => {
  return (
    <div className="border p-2 rounded-md">
      <p className="text-sm font-medium">{marketName}</p>
      <p className="text-lg">{outcomeName}: {odds}</p>
    </div>
  );
};

export default OddsDisplay; 