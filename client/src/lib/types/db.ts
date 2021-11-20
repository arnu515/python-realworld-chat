export interface User {
  id: string;
  created_at: string;
  email: string;
  provider?: "github";
  provider_id?: string;
  provider_data?: Record<string, unknown>;
  profile?: Profile;
}

export interface Profile {
  id: string;
  created_at: string;
  name: string;
  avatar: string;
  bio?: string;
  website?: string;
  user?: User;
}
