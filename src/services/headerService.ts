import api from "./api";

export const searchMedicines = (query: string) =>
  api.get(`/search/?query=${query}`);

export const getNotifications = () =>
  api.get("/notifications/");

export const markNotificationRead = (id: number) =>
  api.put(`/notifications/${id}/read`);

export const deleteNotification = (id: number) =>
  api.delete(`/notifications/${id}`);

export const markAllRead = () =>
  api.put("/notifications/read-all");

export const getProfile = () =>
  api.get("/profile/");

export const updateProfile = (data: any) =>
  api.put("/profile/", data);

export const getSettings = () =>
  api.get("/settings/");

export const saveSettings = (data: any) =>
  api.put("/settings/", data);