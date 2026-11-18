import type { Board, Grade, Role, Stream } from './enums';

/**
 * One card on the "Log in as" persona picker (data/personas/index.json).
 * W1 ships a 3-persona stub; Wave 3 (Personas) replaces the file with the full cast.
 */
export interface PersonaSummary {
  id: string; // lrn_ par_ tch_ csl_ tut_ mnt_ + first_last
  role: Role;
  name: string;
  /** One-line story shown on the card. */
  story: string;
  /** Students only. */
  grade?: Grade;
  board?: Board;
  stream?: Stream;
  /** e.g. "IGCSE", "IB DP 1", "CBSE Science PCM". */
  programme?: string;
  /** Learner IDs this adult is linked to (children, caseload, tutees). */
  linkedLearnerIds?: string[];
  /** Avatar: an image path under /public, or omitted to show initials. */
  avatar?: string;
  /** Picker order within its role group. */
  order?: number;
}
