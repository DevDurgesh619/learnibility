import { describe, expect, it } from 'vitest';
import { markReset, syncResetEpoch, useMemoryOverlay } from './overlay';

describe('reset across instances', () => {
  it('clears once for each newer reset stamp and ignores older or missing ones', () => {
    const ov = useMemoryOverlay();
    ov.put('tasks', 'a', null, { x: 1 });
    expect(syncResetEpoch(undefined)).toBe(false);
    expect(syncResetEpoch(Number('junk'))).toBe(false);
    const epoch = markReset() + 10;
    expect(syncResetEpoch(epoch)).toBe(true);
    expect(ov.count()).toBe(0);
    ov.put('tasks', 'b', null, { x: 2 });
    expect(syncResetEpoch(epoch)).toBe(false);
    expect(syncResetEpoch(epoch - 5)).toBe(false);
    expect(ov.count()).toBe(1);
    expect(syncResetEpoch(epoch + 1)).toBe(true);
    expect(ov.count()).toBe(0);
  });
});
