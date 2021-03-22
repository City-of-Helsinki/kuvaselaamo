import settings from "./settings";

export function getRoute(path: string) {
  return `${settings.baseUrl}${path}`;
}

export function getImageRoute(imageId: string) {
  return getRoute(`/search/details/?image_id=${imageId}`);
}
