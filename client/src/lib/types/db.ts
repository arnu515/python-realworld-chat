export interface User {
  id: string;
  created_at: string;
  email: string;
  provider?: "github" | "password";
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

export interface ChatRequests {
  id: string;
  from_user: {
    id: User["id"];
    email: User["email"];
    profile: User["profile"];
  };
  to_user: ChatRequests["from_user"];
  from_user_id: User["id"];
  to_user_id: User["id"];
  accepted: boolean;
}
