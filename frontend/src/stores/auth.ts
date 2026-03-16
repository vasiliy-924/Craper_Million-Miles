import { create } from "zustand";
import { persist } from "zustand/middleware";
import * as auth from "@/lib/auth";

interface AuthState {
  token: string | null;
  setToken: (token: string) => void;
  clearToken: () => void;
  isAuthenticated: () => boolean;
}

const authStorage: {
  getItem: (name: string) => { state: Pick<AuthState, "token">; version?: number } | null;
  setItem: (name: string, value: { state: Pick<AuthState, "token"> }) => void;
  removeItem: (name: string) => void;
} = {
  getItem: () => {
    const token = auth.getToken();
    return token ? { state: { token }, version: 0 } : null;
  },
  setItem: (_, value) => {
    const token = value?.state?.token;
    if (token) auth.setToken(token);
    else auth.clearToken();
  },
  removeItem: () => auth.clearToken(),
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      setToken: (token) => {
        set({ token });
        auth.setToken(token);
      },
      clearToken: () => {
        set({ token: null });
        auth.clearToken();
      },
      isAuthenticated: () => !!get().token || !!auth.getToken(),
    }),
    { name: "cars-auth", storage: authStorage }
  )
);