import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import { DemoGuide } from '@/components/demo/demo-guide';
import './globals.css';

export const metadata: Metadata = {
  title: 'Learnibility',
  description: 'Hyper-personalised learning for grades 8 to 12',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        {/* Guided demo panel (W3-QA): renders only while a /demo scenario is running. */}
        <DemoGuide />
      </body>
    </html>
  );
}
