/**
 * state.js - Signals-based reactivity for vanilla JavaScript
 *
 * Implements automatic dependency tracking like SolidJS/Preact Signals.
 * Effects automatically re-run when signals they read change.
 *
 * Usage:
 *   const [count, setCount] = createSignal(0);
 *   createEffect(() => {
 *     console.log('Count is:', count());  // auto-tracks dependency
 *   });
 *   setCount(1);  // effect re-runs automatically
 */

// Stack of currently running effects (for auto-tracking)
let currentEffect = null;

/**
 * Creates a reactive signal with automatic dependency tracking.
 * When a signal is read inside an effect, the effect auto-subscribes.
 *
 * @param {T} initialValue - Initial signal value
 * @returns {[() => T, (newValue: T | ((prev: T) => T)) => void]}
 *
 * @example
 * const [count, setCount] = createSignal(0);
 * createEffect(() => console.log(count()));  // logs on every change
 * setCount(1);           // Direct value
 * setCount(c => c + 1);  // Updater function
 */
export function createSignal(initialValue) {
  let value = initialValue;
  const subscribers = new Set();

  // Getter - tracks dependency if inside an effect
  const read = () => {
    if (currentEffect) {
      subscribers.add(currentEffect);
    }
    return value;
  };

  // Setter with support for updater functions
  const write = (newValue) => {
    const nextValue =
      typeof newValue === "function" ? newValue(value) : newValue;

    if (!Object.is(value, nextValue)) {
      value = nextValue;
      // Notify all subscribed effects
      subscribers.forEach((effect) => effect());
    }
  };

  return [read, write];
}

/**
 * Creates an effect that auto-tracks signal dependencies.
 * Re-runs whenever any signal read inside it changes.
 *
 * @param {() => void | (() => void)} fn - Effect function, optionally returns cleanup
 * @returns {() => void} - Dispose function to stop the effect
 *
 * @example
 * const [count, setCount] = createSignal(0);
 * createEffect(() => {
 *   console.log('Count:', count());  // auto-subscribes to count
 * });
 * setCount(5);  // effect runs, logs "Count: 5"
 */
export function createEffect(fn) {
  let cleanup = null;

  const execute = () => {
    // Run cleanup from previous execution
    if (cleanup) cleanup();

    // Set this effect as current (for dependency tracking)
    const prevEffect = currentEffect;
    currentEffect = execute;

    try {
      cleanup = fn() || null;
    } finally {
      currentEffect = prevEffect;
    }
  };

  // Run immediately
  execute();

  // Return dispose function
  return () => {
    if (cleanup) cleanup();
  };
}

/**
 * Creates a computed signal that derives from other signals.
 * Automatically tracks dependencies and recomputes when they change.
 *
 * @param {() => T} computeFn - Function that computes the derived value
 * @returns {() => T} - Getter function for computed value
 *
 * @example
 * const [count, setCount] = createSignal(5);
 * const doubled = createMemo(() => count() * 2);
 * doubled();  // 10
 * setCount(10);
 * doubled();  // 20
 */
export function createMemo(computeFn) {
  const [value, setValue] = createSignal(computeFn());

  createEffect(() => {
    setValue(computeFn());
  });

  return value;
}
