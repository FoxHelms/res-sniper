/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, useEffect, type FormEvent } from "react";

interface Restaurant {
  id: number;
  restName: string;
  venUrl: string;
}

function RestaurantPage() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [userRest, setUserRest] = useState<string>("");

  // Fetch all restaurants
  const fetchRestaurants = async () => {
    try {
      const res = await fetch("/api/restaurants", { credentials: "include" });
      if (!res.ok) throw new Error("Failed to fetch restaurants");
      const data: Restaurant[] = await res.json();
      setRestaurants(data);
    } catch (err) {
      console.error(err);
      alert("Error fetching restaurants");
    }
  };

  useEffect(() => {
    fetchRestaurants();
  }, []);

  // Add a restaurant
  const addRestaurant = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const res = await fetch("/api/restaurants", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userRest }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Error adding restaurant");
      }

      setUserRest("");
      fetchRestaurants();
    } catch (err: any) {
      console.error(err);
      alert(err.message);
    }
  };

  // Delete a restaurant
  const deleteRestaurant = async (id: number) => {
    try {
      const res = await fetch(`/api/restaurants/${id}`, { method: "DELETE" });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Error deleting restaurant");
      }
      fetchRestaurants();
    } catch (err: any) {
      console.error(err);
      alert(err.message);
    }
  };

  return (
    <div className="App">
      <h1>Reservation Sniper</h1>

      {restaurants.length === 0 ? (
        <p>No restaurants yet!</p>
      ) : (
        <ul>
          {restaurants.map((r) => (
            <li key={r.id}>
              <a href={r.venUrl}>{r.restName}</a>{" "}
              <button onClick={() => deleteRestaurant(r.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}

      <form onSubmit={addRestaurant}>
        <input
          type="text"
          value={userRest}
          onChange={(e) => setUserRest(e.target.value)}
          placeholder="Paste link to restaurant"
        />
        <button type="submit">Add Link</button>
      </form>
    </div>
  );
}

export default RestaurantPage;
