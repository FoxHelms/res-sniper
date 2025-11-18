import { useEffect, useState } from "react";
import Login from "./Login";
import RestaurantPage from "./RestaurantPage.tsx"; // your previous App.tsx logic

function App() {
  const [loggedIn, setLoggedIn] = useState<boolean>(false);

  const handleLoginSuccess = () => {
    setLoggedIn(true);
  };

  useEffect(() => {
    const checkLogin = async () => {
      const res = await fetch("/api/me", { credentials: "include" });
      const data = await res.json();
      setLoggedIn(data.loggedIn);
    };

    checkLogin();
  }, []);

  return (
    <div className="App">
      {loggedIn ? (
        <RestaurantPage />
      ) : (
        <Login onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
}

export default App;
