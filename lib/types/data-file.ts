/** Every JSON data file in /data has this envelope. */
export interface DataFile<T> {
  schemaVersion: 1;
  /** Repo-relative path of the script that generated the file. */
  generatedBy: string;
  items: T[];
}
