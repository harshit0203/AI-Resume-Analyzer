import { api } from "./client";
import type {
  Analysis,
  AnalysisListItem,
  AnalysisStats,
  ApiResponse,
  AuthResponse,
  Paginated,
  Resume,
  User,
  UserSettings,
} from "@/lib/types";

export const authApi = {
  async register(payload: { email: string; password: string; full_name: string }) {
    const { data } = await api.post<ApiResponse<AuthResponse>>("/auth/register", payload);
    return data.data;
  },
  async login(payload: { email: string; password: string }) {
    const { data } = await api.post<ApiResponse<AuthResponse>>("/auth/login", payload);
    return data.data;
  },
  async logout() {
    await api.post("/auth/logout");
  },
  async me() {
    const { data } = await api.get<ApiResponse<User>>("/auth/me");
    return data.data;
  },
};

export const userApi = {
  async updateProfile(payload: Partial<Pick<User, "full_name" | "headline" | "avatar_url">>) {
    const { data } = await api.patch<ApiResponse<User>>("/users/me", payload);
    return data.data;
  },
  async changePassword(payload: { current_password: string; new_password: string }) {
    await api.post("/users/me/change-password", payload);
  },
  async getSettings() {
    const { data } = await api.get<ApiResponse<UserSettings>>("/users/me/settings");
    return data.data;
  },
  async updateSettings(payload: Partial<UserSettings>) {
    const { data } = await api.patch<ApiResponse<UserSettings>>("/users/me/settings", payload);
    return data.data;
  },
};

export const resumeApi = {
  async upload(file: File) {
    const form = new FormData();
    form.append("file", file);
    const { data } = await api.post<ApiResponse<Resume>>("/resumes", form, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return data.data;
  },
  async list(params: { page?: number; page_size?: number; search?: string } = {}) {
    const { data } = await api.get<Paginated<Resume>>("/resumes", { params });
    return data;
  },
  async get(id: string) {
    const { data } = await api.get<ApiResponse<Resume>>(`/resumes/${id}`);
    return data.data;
  },
  async setPrimary(id: string) {
    const { data } = await api.post<ApiResponse<Resume>>(`/resumes/${id}/primary`);
    return data.data;
  },
  async remove(id: string) {
    await api.delete(`/resumes/${id}`);
  },
  downloadUrl(id: string) {
    return `${api.defaults.baseURL}/resumes/${id}/download`;
  },
};

export const analysisApi = {
  async create(payload: { resume_id: string; target_role?: string }) {
    const { data } = await api.post<ApiResponse<Analysis>>("/analyses", payload);
    return data.data;
  },
  async list(params: { page?: number; page_size?: number; resume_id?: string } = {}) {
    const { data } = await api.get<Paginated<AnalysisListItem>>("/analyses", { params });
    return data;
  },
  async get(id: string) {
    const { data } = await api.get<ApiResponse<Analysis>>(`/analyses/${id}`);
    return data.data;
  },
  async stats() {
    const { data } = await api.get<ApiResponse<AnalysisStats>>("/analyses/stats");
    return data.data;
  },
  async remove(id: string) {
    await api.delete(`/analyses/${id}`);
  },
};
