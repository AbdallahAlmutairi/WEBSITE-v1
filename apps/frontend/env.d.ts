interface ImportMetaEnv {
  readonly NEXT_PUBLIC_API_BASE: string;
}

declare namespace NodeJS {
  interface ProcessEnv extends ImportMetaEnv {}
}
