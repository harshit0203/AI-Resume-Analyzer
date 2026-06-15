/** Shared TypeScript types mirroring the backend API contracts. */

export type UserRole = "user" | "admin";
export type SubscriptionPlan = "free" | "pro" | "enterprise";
export type ResumeStatus = "uploaded" | "parsing" | "parsed" | "failed";
export type AnalysisStatus = "pending" | "running" | "completed" | "failed";
export type AgentStatus = "pending" | "running" | "completed" | "failed";

export type AgentType =
  | "resume_parser"
  | "ats_analyzer"
  | "skill_gap"
  | "job_match"
  | "resume_improvement"
  | "career_coach";

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface PageMeta {
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface Paginated<T> {
  success: boolean;
  items: T[];
  meta: PageMeta;
}

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  avatar_url: string | null;
  headline: string | null;
  role: UserRole;
  plan: SubscriptionPlan;
  is_active: boolean;
  is_verified: boolean;
  last_login_at: string | null;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface UserSettings {
  theme: string;
  default_target_role: string | null;
  email_notifications: boolean;
  product_updates: boolean;
  analysis_complete_alerts: boolean;
  locale: string;
  timezone: string;
}

export interface Resume {
  id: string;
  file_name: string;
  content_type: string;
  file_size: number;
  status: ResumeStatus;
  version: number;
  is_primary: boolean;
  parsed_data?: ParsedResume | null;
  parse_error?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ParsedResume {
  contact: {
    name?: string | null;
    email?: string | null;
    phone?: string | null;
    location?: string | null;
    links: string[];
  };
  summary?: string | null;
  skills: string[];
  education: Array<Record<string, unknown>>;
  experience: Array<Record<string, unknown>>;
  certifications: string[];
  projects: Array<Record<string, unknown>>;
  languages: string[];
  total_experience_years?: number | null;
}

export interface AgentExecution {
  id: string;
  agent_type: AgentType;
  sequence: number;
  status: AgentStatus;
  output?: Record<string, unknown> | null;
  error?: string | null;
  tokens_used?: number | null;
  duration_ms?: number | null;
  started_at?: string | null;
  completed_at?: string | null;
}

export interface JobMatch {
  id: string;
  title: string;
  company_type?: string | null;
  match_percentage: number;
  seniority?: string | null;
  salary_range?: string | null;
  reasons: string[];
  missing_skills: string[];
  matched_skills: string[];
  description?: string | null;
}

export interface CareerInsight {
  id: string;
  current_level?: string | null;
  target_role?: string | null;
  salary_insights?: Record<string, unknown> | null;
  next_steps: string[];
  recommended_certifications: string[];
  learning_plan: Array<Record<string, unknown>>;
  growth_recommendations: string[];
  roadmap: Array<Record<string, unknown>>;
  narrative?: string | null;
}

export interface ATSResult {
  ats_score: number;
  strengths: string[];
  weaknesses: string[];
  missing_keywords: string[];
  recommendations: string[];
  formatting_issues: string[];
}

export interface SkillGapResult {
  target_path?: string;
  matched_skills: string[];
  missing_skills: Array<{ skill: string; importance: string; resources: string[] }>;
  coverage_percentage: number;
  learning_roadmap: Array<Record<string, unknown>>;
}

export interface ImprovementResult {
  improved_summary?: string;
  stronger_bullets: Array<{ before: string; after: string }>;
  achievement_suggestions: string[];
  project_suggestions: string[];
  ats_keywords: string[];
}

export interface Analysis {
  id: string;
  resume_id: string;
  status: AnalysisStatus;
  target_role?: string | null;
  ats_score?: number | null;
  overall_score?: number | null;
  ats_result?: ATSResult | null;
  skill_gap_result?: SkillGapResult | null;
  improvement_result?: ImprovementResult | null;
  summary?: string | null;
  error?: string | null;
  duration_ms?: number | null;
  started_at?: string | null;
  completed_at?: string | null;
  created_at: string;
  agent_executions: AgentExecution[];
  job_matches: JobMatch[];
  career_insight?: CareerInsight | null;
}

export interface AnalysisListItem {
  id: string;
  resume_id: string;
  status: AnalysisStatus;
  target_role?: string | null;
  ats_score?: number | null;
  overall_score?: number | null;
  created_at: string;
  completed_at?: string | null;
}

export interface AnalysisStats {
  total_analyses: number;
  average_ats_score: number;
  best_ats_score: number;
}

export interface WsAgentUpdate {
  type: "connected" | "analysis_started" | "agent_update" | "analysis_completed";
  analysis_id: string;
  agent?: AgentType;
  status?: string;
  sequence?: number | null;
  data?: Record<string, unknown> | null;
  agents?: AgentType[];
  ats_score?: number | null;
  overall_score?: number | null;
}

export const CAREER_PATHS = [
  "MERN Developer",
  "Full Stack Engineer",
  "AI Engineer",
  "DevOps Engineer",
  "Python Developer",
  "Java Developer",
] as const;

export const AGENT_META: Record<AgentType, { label: string; description: string }> = {
  resume_parser: { label: "Resume Parser", description: "Extracts structured data from your resume" },
  ats_analyzer: { label: "ATS Analyzer", description: "Scores ATS compatibility & keywords" },
  skill_gap: { label: "Skill Gap", description: "Compares skills to your target path" },
  job_match: { label: "Job Match", description: "Finds best-fit roles with match scores" },
  resume_improvement: { label: "Resume Improvement", description: "Rewrites bullets & summary" },
  career_coach: { label: "Career Coach", description: "Salary, roadmap & growth plan" },
};
