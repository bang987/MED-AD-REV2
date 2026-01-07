// MedAdReview Type Definitions

// Verdict types
export type VerdictType = "allow" | "conditional" | "deny" | "hold";

// Severity levels
export type SeverityLevel = "critical" | "high" | "medium" | "low";

// Review status
export type ReviewStatus = "pending" | "processing" | "completed" | "failed";

// User roles
export type UserRole = "admin" | "reviewer" | "viewer";

// API Response wrapper
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
}

// Pagination
export interface PaginationParams {
  page: number;
  size: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}
