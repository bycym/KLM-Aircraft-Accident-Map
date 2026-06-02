export interface RuntimeConfig {
  apiBaseUrl: string;
  tileUrl: string;
}

declare global {
  interface Window {
    SAFETY_CONFIG?: Partial<RuntimeConfig>;
  }
}

export const DEFAULT_CONFIG: RuntimeConfig = {
  apiBaseUrl: 'http://localhost:8000',
  tileUrl: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
};

export function getRuntimeConfig(): RuntimeConfig {
  return { ...DEFAULT_CONFIG, ...(window.SAFETY_CONFIG ?? {}) };
}
