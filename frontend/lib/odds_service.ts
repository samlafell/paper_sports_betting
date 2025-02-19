import { OddsUpdate } from '../types/betting'; // Import your type

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'; // Or your API base URL

export const connectToOddsStream = (eventId: string, onOddsUpdate: (odds: OddsUpdate) => void) => {
  const eventSource = new EventSource(`${API_BASE_URL}/odds/${eventId}`);

  eventSource.onmessage = (event) => {
    try {
      const odds: OddsUpdate = JSON.parse(event.data);
      onOddsUpdate(odds); // Call the callback function with the updated odds
    } catch (error) {
      console.error("Error parsing odds data:", error);
      // Handle the error appropriately (e.g., display an error message)
    }
  };

  eventSource.onerror = (error) => {
      console.error("Error with odds stream:", error);
      // Handle error, maybe retry connection after some time
      eventSource.close(); // Close the connection if necessary
      // Consider implementing a reconnect strategy
  };

  return () => { // Return a cleanup function
    eventSource.close();
  };
};