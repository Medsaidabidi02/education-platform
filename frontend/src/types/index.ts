export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: 'student' | 'instructor' | 'admin';
  phone_number?: string;
  date_of_birth?: string;
  profile_picture?: string;
  bio?: string;
  is_approved: boolean;
  max_devices: number;
  created_at: string;
  updated_at: string;
}

export interface Plan {
  id: number;
  name: string;
  description: string;
  plan_type: 'basic' | 'premium' | 'enterprise';
  price: number;
  currency: string;
  max_courses: number;
  max_videos_per_course: number;
  max_devices: number;
  video_quality: string;
  download_enabled: boolean;
  offline_viewing: boolean;
  duration_days: number;
  is_active: boolean;
  is_popular: boolean;
  created_at: string;
  updated_at: string;
}

export interface Course {
  id: number;
  title: string;
  description: string;
  short_description: string;
  slug: string;
  instructor: User;
  category?: Category;
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  thumbnail?: string;
  preview_video?: string;
  required_plans: Plan[];
  is_free: boolean;
  price: number;
  duration_hours: number;
  total_lessons: number;
  status: 'draft' | 'published' | 'archived';
  is_featured: boolean;
  tags: string;
  average_rating: number;
  total_reviews: number;
  created_at: string;
  updated_at: string;
  published_at?: string;
}

export interface Category {
  id: number;
  name: string;
  description: string;
  slug: string;
  icon: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Video {
  id: number;
  title: string;
  description: string;
  course: number;
  order: number;
  duration_seconds: number;
  file_size: number;
  video_file?: string;
  thumbnail?: string;
  quality: '480p' | '720p' | '1080p' | '4k';
  video_id: string;
  encrypted_url?: string;
  is_preview: boolean;
  is_downloadable: boolean;
  status: 'processing' | 'ready' | 'failed' | 'archived';
  processing_progress: number;
  view_count: number;
  duration_formatted: string;
  created_at: string;
  updated_at: string;
}

export interface Review {
  id: number;
  user: User;
  course: number;
  rating: number;
  title: string;
  comment: string;
  status: 'pending' | 'approved' | 'rejected';
  is_approved: boolean;
  moderator?: User;
  moderation_notes: string;
  helpful_count: number;
  not_helpful_count: number;
  helpfulness_ratio: number;
  created_at: string;
  updated_at: string;
  moderated_at?: string;
}

export interface LoginData {
  email: string;
  password: string;
  device_fingerprint?: string;
}

export interface RegisterData {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  password: string;
  password_confirm: string;
  phone_number?: string;
  date_of_birth?: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
  session_id: number;
}

export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
}

export interface ApiErrorResponse {
  response?: {
    data?: {
      error?: string;
      message?: string;
    };
  };
}