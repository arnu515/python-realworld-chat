import type { Profile, User } from "$lib/types/db";
import { writable } from "svelte/store";

export interface UserProfile extends User {
  profile: Profile;
}

export const user = writable<UserProfile>(null);
