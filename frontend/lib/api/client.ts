import axios, {
  type AxiosError,
  type AxiosInstance,
  type InternalAxiosRequestConfig,
} from "axios";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const API_V1 = `${API_BASE_URL}/api/v1`;

export interface ApiError {
  code: string;
  message: string;
  details?: unknown;
}

/**
 * Centralised Axios instance.
 *
 * Auth is cookie-based: the backend sets httpOnly access + refresh cookies, so
 * `withCredentials: true` is sufficient for the browser to authenticate every
 * request. A response interceptor transparently refreshes the access token on a
 * 401 and retries the original request exactly once.
 */
export const api: AxiosInstance = axios.create({
  baseURL: API_V1,
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
  timeout: 30000,
});

let isRefreshing = false;
let pendingQueue: Array<(ok: boolean) => void> = [];

function flushQueue(ok: boolean) {
  pendingQueue.forEach((resolve) => resolve(ok));
  pendingQueue = [];
}

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    const status = error.response?.status;
    const url = original?.url ?? "";

    const isAuthRoute =
      url.includes("/auth/login") ||
      url.includes("/auth/register") ||
      url.includes("/auth/refresh");

    if (status === 401 && original && !original._retry && !isAuthRoute) {
      original._retry = true;

      if (isRefreshing) {
        const ok = await new Promise<boolean>((resolve) => pendingQueue.push(resolve));
        if (!ok) return Promise.reject(error);
        return api(original);
      }

      isRefreshing = true;
      try {
        await api.post("/auth/refresh");
        flushQueue(true);
        return api(original);
      } catch (refreshError) {
        flushQueue(false);
        if (typeof window !== "undefined" && !window.location.pathname.startsWith("/login")) {
          window.location.href = "/login";
        }
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

/** Normalise an axios error into a friendly message. */
export function extractError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const payload = error.response?.data as { error?: ApiError } | undefined;
    if (payload?.error) return payload.error;
    return { code: "network_error", message: error.message };
  }
  return { code: "unknown", message: "An unexpected error occurred." };
}
