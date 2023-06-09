import settings from "./settings";

export function getRoute(path: string) {
  return `${settings.baseUrl}/language/?lang=en&next=${path}`;
}

export function getImageRoute(imageId: string) {
  return getRoute(`/search/details/?image_id=${imageId}`);
}
