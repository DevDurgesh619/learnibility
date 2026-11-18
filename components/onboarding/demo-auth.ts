/**
 * Demo sign-in (PDF 1b-1c). No SMS is sent: every number gets the same one-time code.
 * Numbers listed here belong to returning demo personas and skip onboarding (1c → Home);
 * any other number is a new student and becomes the demo's new user, Zoya Fernandes.
 */
export const DEMO_OTP = '246810';

export const NEW_STUDENT_PERSONA_ID = 'lrn_zoya_fernandes';
export const NEW_STUDENT_DEMO_PHONE = '9876543210';

export const RETURNING_PHONES: Record<string, string> = {
  '9811000001': 'lrn_kabir_singh',
  '9811000002': 'lrn_ishita_rao',
  '9811000003': 'lrn_nikhil_reddy',
};

export function normalisePhone(raw: string): string {
  const digits = raw.replace(/\D/g, '');
  return digits.length > 10 && digits.startsWith('91') ? digits.slice(-10) : digits;
}

export function isValidIndianMobile(phone: string): boolean {
  return /^[6-9]\d{9}$/.test(phone);
}

export function formatPhone(phone: string): string {
  return phone.length === 10 ? `+91 ${phone.slice(0, 5)} ${phone.slice(5)}` : phone;
}
