/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, type FormEvent } from "react";

interface LoginProps {
  onLoginSuccess: () => void;
}

const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const res = await fetch("/api/login", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ResyEmail: email, ResyPW: password }),
      });

      let data;

      try {
        data = await res.json(); // only read once
      } catch {
        data = { error: "Invalid server response" };
      }

      if (!res.ok) {
        throw new Error(data.error || "Login failed");
      }

      console.log("Login success:", data.message);
      onLoginSuccess();
    } catch (err: any) {
      alert(err.message);
    }
  };

  return (
    <div className="Login">
      <h1>Login to Resy</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
