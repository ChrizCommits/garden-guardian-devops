import { useEffect, useMemo, useState } from "react";
import { api } from "./api/client";
import AnimalGuide from "./components/AnimalGuide";
import CardCollection from "./components/CardCollection";
import Dashboard from "./components/Dashboard";
import DemoLogin from "./components/DemoLogin";
import Profile from "./components/Profile";
import type { User } from "./types/api";

const STORAGE_KEY = "gardenguardian.demoUser";

type Route = "/" | "/login" | "/profile" | "/cards" | "/animals";

function currentRoute(): Route {
  const path = window.location.pathname;
  if (path === "/profile" || path === "/cards" || path === "/animals" || path === "/login") {
    return path;
  }
  return "/";
}

export default function App() {
  const [route, setRoute] = useState<Route>(currentRoute());
  const [user, setUser] = useState<User | null>(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? (JSON.parse(stored) as User) : null;
  });

  useEffect(() => {
    const onPop = () => setRoute(currentRoute());
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, []);

  useEffect(() => {
    if (!user) {
      return;
    }
    api.getMe(user.id).then(setUser).catch(() => {
      localStorage.removeItem(STORAGE_KEY);
      setUser(null);
      navigate("/login");
    });
  }, []);

  function navigate(nextRoute: Route) {
    window.history.pushState({}, "", nextRoute);
    setRoute(nextRoute);
  }

  function handleLogin(nextUser: User) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(nextUser));
    setUser(nextUser);
    navigate("/");
  }

  function handleUserUpdate(nextUser: User) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(nextUser));
    setUser(nextUser);
  }

  function logout() {
    localStorage.removeItem(STORAGE_KEY);
    setUser(null);
    navigate("/login");
  }

  const page = useMemo(() => {
    if (!user || route === "/login") {
      return <DemoLogin onLogin={handleLogin} />;
    }
    if (route === "/profile") {
      return <Profile user={user} />;
    }
    if (route === "/cards") {
      return <CardCollection user={user} />;
    }
    if (route === "/animals") {
      return <AnimalGuide />;
    }
    return <Dashboard user={user} onUserUpdate={handleUserUpdate} />;
  }, [route, user]);

  return (
    <div className="app-shell">
      <header className="topbar">
        <button className="brand" type="button" onClick={() => navigate("/")}>
          <span className="brand-mark">GG</span>
          <span>
            <strong>GardenGuardian</strong>
            <small>Small daily actions for garden wildlife</small>
          </span>
        </button>
        {user ? (
          <nav className="nav-links" aria-label="Main navigation">
            <button type="button" onClick={() => navigate("/")}>Today</button>
            <button type="button" onClick={() => navigate("/profile")}>Profile</button>
            <button type="button" onClick={() => navigate("/cards")}>Cards</button>
            <button type="button" onClick={() => navigate("/animals")}>Animals</button>
            <button className="quiet" type="button" onClick={logout}>Switch user</button>
          </nav>
        ) : null}
      </header>
      <main>{page}</main>
    </div>
  );
}
