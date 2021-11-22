import type { Profile, User } from "$lib/types/db";
import axios, { AxiosError } from "axios";
import { writable } from "svelte/store";

export interface UserProfile extends User {
  profile: Profile;
}

export function fetchUser(): Promise<void> {
  return axios
    .get("/api/auth/me")
    .then(({ data }) => {
      user.set(data.user);
    })
    .catch((e: AxiosError) => {
      if (e.response.status === 401) {
        user.set(null);
      } else {
        throw e;
      }
    });
}

export const user = writable<UserProfile>(null);
