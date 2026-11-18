/**
 * View models shared by the test player and result screens (W2-S1).
 * Built on the server from `Question`s; the player never sees answers unless the test is adaptive.
 */

export type PlayerItemKind = 'mcq' | 'text' | 'numerical';

export interface PlayerItem {
  id: string;
  /** Section label shown above the stem, e.g. "Geometry" or "Part B · Reasoning". */
  topic: string;
  kind: PlayerItemKind;
  stem: string;
  options?: string[];
  /** Inline SVG figure (reasoning items). Trusted: authored in our own data files. */
  svg?: string;
  marks: number;
  /** Suggested minutes for this item. */
  minutes: number;
}

export interface PlayerResponse {
  questionId: string;
  /** Empty string or undefined means left blank. */
  answer?: string;
  secondsTaken: number;
  confidence?: 1 | 2 | 3 | 4 | 5;
  flagged?: boolean;
}

export interface PlayerSubmission {
  responses: PlayerResponse[];
  /** Seconds from start to submit. */
  elapsedSeconds: number;
  autoSubmitted: boolean;
}
