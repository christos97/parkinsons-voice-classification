/**
 * state.js - Signals-based reactivity for vanilla JavaScript
 *
 * Implements automatic dependency tracking like SolidJS Signals.
 * Effects automatically re-run when signals they read change.
 *
 * @see https://docs.solidjs.com/reference/basic-reactivity/create-signal
 * @see https://docs.solidjs.com/reference/basic-reactivity/create-effect
 * @see https://docs.solidjs.com/reference/basic-reactivity/create-memo
 */

// ============================================================
// Type Definitions (JSDoc)
// ============================================================

/**
 * @template T
 * @typedef {() => T} Accessor - Reactive getter function
 */

/**
 * @template T
 * @callback Setter
 * @param {T | ((prev: T) => T)} value - New value or updater function
 * @returns {T} The new value
 */

/**
 * @template T
 * @typedef {[get: Accessor<T>, set: Setter<T>]} Signal
 */

/**
 * @template T
 * @typedef {Object} SignalOptions
 * @property {string} [name] - Debug name for the signal
 * @property {false | ((prev: T, next: T) => boolean)} [equals] - Custom equality function (default: Object.is). Set to `false` to always notify.
 */

/**
 * @template T
 * @callback EffectFunction
 * @param {T} v - Previous value (or initial value on first run)
 * @returns {T} Next value to pass to subsequent runs
 */

/**
 * @typedef {Object} EffectOptions
 * @property {string} [name] - Debug name for the effect
 */

/**
 * @template T
 * @typedef {Object} MemoOptions
 * @property {string} [name] - Debug name for the memo
 * @property {false | ((prev: T, next: T) => boolean)} [equals] - Custom equality function (default: Object.is). Set to `false` to always update.
 */

// ============================================================
// Internal State
// ============================================================

/** @type {(() => void) | null} */
let currentEffect = null;

// ============================================================
// createSignal
// ============================================================

/**
 * Creates a reactive signal with automatic dependency tracking.
 *
 * @template T
 * @overload
 * @returns {Signal<T | undefined>}
 */
/**
 * @template T
 * @overload
 * @param {T} value - Initial signal value
 * @param {SignalOptions<T>} [options] - Signal options
 * @returns {Signal<T>}
 */
/**
 * @template T
 * @param {T} [value] - Initial signal value
 * @param {SignalOptions<T>} [options] - Signal options
 * @returns {Signal<T>}
 *
 * @example
 * const [count, setCount] = createSignal(0);
 * createEffect(() => console.log(count()));
 * setCount(1);           // Direct value
 * setCount(c => c + 1);  // Updater function
 *
 * @example
 * // Custom equality
 * const [obj, setObj] = createSignal({ x: 1 }, {
 *   equals: (prev, next) => prev.x === next.x
 * });
 *
 * @example
 * // Always notify (no equality check)
 * const [val, setVal] = createSignal(0, { equals: false });
 */
export function createSignal(value, options) {
  const equals = options?.equals;
  const subscribers = new Set();

  /** @type {Accessor<T>} */
  const read = () => {
    if (currentEffect) {
      subscribers.add(currentEffect);
    }
    return value;
  };

  /** @type {Setter<T>} */
  const write = (newValue) => {
    const nextValue =
      typeof newValue === "function" ? newValue(value) : newValue;

    // Determine if we should update
    const shouldUpdate =
      equals === false
        ? true
        : equals
          ? !equals(value, nextValue)
          : !Object.is(value, nextValue);

    if (shouldUpdate) {
      value = nextValue;
      // Notify all subscribed effects (copy to avoid mutation during iteration)
      [...subscribers].forEach((effect) => effect());
    }

    return nextValue;
  };

  return [read, write];
}

// ============================================================
// createEffect
// ============================================================

/**
 * Creates an effect that auto-tracks signal dependencies.
 * Re-runs whenever any signal read inside it changes.
 *
 * @template [T=void]
 * @overload
 * @param {EffectFunction<T | undefined>} fn - Effect function
 * @returns {void}
 */
/**
 * @template T
 * @overload
 * @param {EffectFunction<T>} fn - Effect function receiving previous value
 * @param {T} value - Initial value for first execution
 * @param {EffectOptions} [options] - Effect options
 * @returns {void}
 */
/**
 * @template T
 * @param {EffectFunction<T>} fn - Effect function
 * @param {T} [value] - Initial value
 * @param {EffectOptions} [options] - Effect options
 * @returns {void}
 *
 * @example
 * // Simple effect (no value tracking)
 * const [count, setCount] = createSignal(0);
 * createEffect(() => {
 *   console.log('Count:', count());
 * });
 *
 * @example
 * // Effect with value tracking
 * createEffect((prev) => {
 *   const next = count();
 *   console.log('Changed from', prev, 'to', next);
 *   return next;
 * }, 0);
 */
export function createEffect(fn, value, options) {
  const execute = () => {
    const prevEffect = currentEffect;
    currentEffect = execute;

    try {
      value = fn(value);
    } finally {
      currentEffect = prevEffect;
    }
  };

  // Run immediately
  execute();
}

// ============================================================
// createMemo
// ============================================================

/**
 * Creates a computed/derived signal that automatically tracks dependencies.
 * The memo only recomputes when its dependencies change.
 *
 * @template T
 * @param {(prev: T) => T} fn - Computation function receiving previous value
 * @param {T} [value] - Initial seed value (passed to fn on first run)
 * @param {MemoOptions<T>} [options] - Memo options
 * @returns {Accessor<T>} - Read-only accessor for the computed value
 *
 * @example
 * const [count, setCount] = createSignal(5);
 * const doubled = createMemo(() => count() * 2);
 * doubled();  // 10
 * setCount(10);
 * doubled();  // 20
 *
 * @example
 * // With initial value
 * const sum = createMemo((prev) => prev + count(), 0);
 *
 * @example
 * // Custom equality
 * const data = createMemo(() => fetchData(), undefined, {
 *   equals: (a, b) => a?.id === b?.id
 * });
 */
export function createMemo(fn, value, options) {
  const equals = options?.equals;

  const [memo, setMemo] = createSignal(value, { equals });

  createEffect(() => {
    setMemo((prev) => fn(prev));
  });

  return memo;
}
