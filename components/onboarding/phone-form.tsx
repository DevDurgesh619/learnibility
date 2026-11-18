'use client';

import { useActionState, useState } from 'react';
import { Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { requestOtp } from '@/lib/actions/onboarding';
import { NEW_STUDENT_DEMO_PHONE, RETURNING_PHONES } from './demo-auth';

export function PhoneForm() {
  const [state, action, pending] = useActionState(requestOtp, {});
  const [phone, setPhone] = useState('');
  return (
    <Card className="p-6">
      <h1 className="text-xl font-semibold text-ink">Enter your mobile number</h1>
      <p className="mt-1 text-sm text-muted">We&apos;ll send a one-time code. New here? Same door.</p>
      <form action={action} className="mt-5 flex flex-col gap-3">
        <div className="flex gap-2">
          <span className="flex h-11 items-center rounded-lg border border-line bg-surface-muted px-3 text-sm text-muted">+91</span>
          <input
            name="phone"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            inputMode="numeric"
            autoComplete="tel-national"
            placeholder="98765 43210"
            aria-label="Mobile number"
            aria-invalid={!!state.error}
            className="h-11 flex-1 rounded-lg border border-line bg-surface px-3 text-base outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-200"
          />
        </div>
        {state.error && <p className="text-sm text-danger-700" role="alert">{state.error}</p>}
        <Button type="submit" size="lg" disabled={pending}>
          {pending && <Loader2 className="animate-spin" />} Send OTP
        </Button>
        <p className="text-xs text-subtle">By continuing you agree to the Terms and Privacy Policy.</p>
      </form>
      <div className="mt-5 rounded-lg bg-surface-muted p-3 text-xs text-muted">
        <p className="font-medium text-ink">Demo numbers</p>
        <button type="button" className="mt-1 block text-left text-brand-700 hover:underline" onClick={() => setPhone(NEW_STUDENT_DEMO_PHONE)}>
          {NEW_STUDENT_DEMO_PHONE.slice(0, 5)} {NEW_STUDENT_DEMO_PHONE.slice(5)} · new student (Zoya)
        </button>
        {Object.keys(RETURNING_PHONES).slice(0, 1).map((p) => (
          <button key={p} type="button" className="mt-1 block text-left text-brand-700 hover:underline" onClick={() => setPhone(p)}>
            {p.slice(0, 5)} {p.slice(5)} · returning student (Kabir)
          </button>
        ))}
      </div>
    </Card>
  );
}
