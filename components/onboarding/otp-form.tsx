'use client';

import { useActionState, useEffect, useRef, useState } from 'react';
import Link from 'next/link';
import { Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { verifyOtp } from '@/lib/actions/onboarding';
import { DEMO_OTP, formatPhone } from './demo-auth';

const RESEND_SECONDS = 30;

export function OtpForm({ phone }: { phone: string }) {
  const [state, action, pending] = useActionState(verifyOtp, {});
  const [digits, setDigits] = useState<string[]>(Array(6).fill(''));
  const [wait, setWait] = useState(RESEND_SECONDS);
  const [resent, setResent] = useState(false);
  const refs = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    if (wait <= 0) return;
    const t = setTimeout(() => setWait((w) => w - 1), 1000);
    return () => clearTimeout(t);
  }, [wait]);

  useEffect(() => refs.current[0]?.focus(), []);

  const set = (i: number, v: string) => {
    const clean = v.replace(/\D/g, '');
    if (clean.length > 1) {
      // Paste of the whole code.
      const next = clean.slice(0, 6).split('');
      setDigits([...next, ...Array(6 - next.length).fill('')]);
      refs.current[Math.min(5, next.length)]?.focus();
      return;
    }
    setDigits((d) => d.map((x, j) => (j === i ? clean : x)));
    if (clean && i < 5) refs.current[i + 1]?.focus();
  };

  return (
    <Card className="p-6">
      <h1 className="text-xl font-semibold text-ink">Enter the 6-digit code</h1>
      <p className="mt-1 text-sm text-muted">
        Sent to {formatPhone(phone)} ·{' '}
        <Link href="/signup" className="text-brand-700 hover:underline">Change</Link>
      </p>
      <form action={action} className="mt-5 flex flex-col gap-3">
        <input type="hidden" name="phone" value={phone} />
        <input type="hidden" name="code" value={digits.join('')} />
        <div className="grid grid-cols-6 gap-2" role="group" aria-label="One-time code">
          {digits.map((d, i) => (
            <input
              key={i}
              ref={(el) => {
                refs.current[i] = el;
              }}
              value={d}
              onChange={(e) => set(i, e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Backspace' && !d && i > 0) refs.current[i - 1]?.focus();
              }}
              inputMode="numeric"
              autoComplete={i === 0 ? 'one-time-code' : 'off'}
              maxLength={6}
              aria-label={`Digit ${i + 1}`}
              className={cn(
                'h-12 w-full rounded-lg border bg-surface text-center text-lg font-semibold outline-none focus:ring-2',
                state.error ? 'border-danger-600 focus:ring-danger-600/20' : 'border-line focus:border-brand-500 focus:ring-brand-200',
              )}
            />
          ))}
        </div>
        {state.error && <p className="text-sm text-danger-700" role="alert">{state.error}</p>}
        <Button type="submit" size="lg" disabled={pending || digits.join('').length < 6}>
          {pending && <Loader2 className="animate-spin" />} Verify
        </Button>
        <p className="text-sm text-muted">
          {wait > 0 ? (
            <>Resend code in 0:{String(wait).padStart(2, '0')}</>
          ) : (
            <button type="button" className="text-brand-700 hover:underline" onClick={() => { setWait(RESEND_SECONDS); setResent(true); }}>
              Resend code
            </button>
          )}
          {resent && wait > 0 && <span className="ml-2 text-success-700">New code sent.</span>}
        </p>
      </form>
      <div className="mt-5 flex items-center justify-between rounded-lg bg-surface-muted p-3 text-xs text-muted">
        <span>Demo: no SMS is sent. The code is <span className="font-semibold text-ink">{DEMO_OTP}</span>.</span>
        <button type="button" className="text-brand-700 hover:underline" onClick={() => setDigits(DEMO_OTP.split(''))}>Fill</button>
      </div>
    </Card>
  );
}
