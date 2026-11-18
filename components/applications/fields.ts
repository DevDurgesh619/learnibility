/** Display labels for programme fields. Plain module so server and client components can both call it. */
const FIELD_LABEL: Record<string, string> = {
  'computer-science': 'Computer science', economics: 'Economics', business: 'Business', accounting: 'Accounting', commerce: 'Commerce',
  medicine: 'Medicine', law: 'Law', psychology: 'Psychology', 'mechanical-engineering': 'Mechanical eng.', 'electrical-engineering': 'Electrical eng.',
  architecture: 'Architecture', design: 'Design', 'data-science': 'Data science', politics: 'Politics', 'liberal-arts': 'Liberal arts', finance: 'Finance',
};
export const fieldLabel = (f: string) => FIELD_LABEL[f] ?? f.replace(/-/g, ' ').replace(/^\w/, (c) => c.toUpperCase());
