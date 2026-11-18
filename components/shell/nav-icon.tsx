import {
  AlertTriangle, Briefcase, Calendar, ChartLine, ClipboardList, Clock, Compass, FileText, Folder, GraduationCap, Grid3x3,
  Home, Layers, List, MessageSquare, Send, Shield, Star, User, Users, Video, Wallet, type LucideIcon,
} from 'lucide-react';
import type { NavIcon as NavIconKey } from '@/lib/nav';

const ICONS: Record<NavIconKey, LucideIcon> = {
  home: Home, calendar: Calendar, folder: Folder, users: Users, graduation: GraduationCap, clipboard: ClipboardList,
  compass: Compass, video: Video, chart: ChartLine, wallet: Wallet, briefcase: Briefcase, message: MessageSquare,
  shield: Shield, layers: Layers, send: Send, grid: Grid3x3, user: User, list: List, alert: AlertTriangle,
  file: FileText, clock: Clock, star: Star,
};

export function NavIcon({ name, className }: { name: NavIconKey; className?: string }) {
  const Icon = ICONS[name];
  return <Icon className={className} aria-hidden />;
}
