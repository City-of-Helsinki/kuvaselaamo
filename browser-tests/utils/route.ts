import settings from "./settings";

export function getRoute(path: string) {
  return `${settings.baseUrl}${path}`;
}
