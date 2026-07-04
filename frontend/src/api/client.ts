import type { Animal, CompleteResult, EarnedAnimalCard, Profile, TodayTip, User } from "../types/api";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const api = {
  demoLogin(username: string) {
    return request<User>("/api/auth/demo-login", {
      method: "POST",
      body: JSON.stringify({ username })
    });
  },
  getMe(userId: number) {
    return request<User>(`/api/auth/me?user_id=${userId}`);
  },
  getToday() {
    return request<TodayTip>("/api/today");
  },
  intendTip(tipId: number, userId: number) {
    return request<{ message: string; awarded: boolean }>(`/api/tips/${tipId}/intend`, {
      method: "POST",
      body: JSON.stringify({ user_id: userId })
    });
  },
  completeTip(tipId: number, userId: number) {
    return request<CompleteResult>(`/api/tips/${tipId}/complete`, {
      method: "POST",
      body: JSON.stringify({ user_id: userId })
    });
  },
  getProfile(userId: number) {
    return request<Profile>(`/api/profile?user_id=${userId}`);
  },
  getCards(userId: number) {
    return request<{ cards: EarnedAnimalCard[] }>(`/api/cards?user_id=${userId}`);
  },
  getAnimals() {
    return request<Animal[]>("/api/animals");
  }
};
