# Document E-Signature Design System

## Design Principles

### 1. Clarity First
Every interface element should have a clear purpose and communicate its function immediately.

### 2. Trust Through Transparency
Build confidence through consistent visual hierarchy and clear status indicators.

### 3. Accessible Simplicity
Maintain simplicity without sacrificing functionality or accessibility.

## Color Palette

### Primary Colors
```css
--primary-50: #eff6ff;   /* Lightest blue */
--primary-100: #dbeafe;
--primary-200: #bfdbfe;
--primary-500: #3b82f6;  /* Main brand blue */
--primary-600: #2563eb;
--primary-700: #1d4ed8;
--primary-800: #1e40af;
--primary-900: #1e3a8a;
```

### Semantic Colors
```css
--success-50: #f0fdf4;
--success-500: #22c55e;
--success-600: #16a34a;

--warning-50: #fefce8;
--warning-500: #eab308;
--warning-600: #ca8a04;

--danger-50: #fef2f2;
--danger-500: #ef4444;
--danger-600: #dc2626;

--info-50: #f0f9ff;
--info-500: #06b6d4;
--info-600: #0891b2;
```

### Neutral Colors
```css
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-200: #e5e7eb;
--gray-300: #d1d5db;
--gray-400: #9ca3af;
--gray-500: #6b7280;
--gray-600: #4b5563;
--gray-700: #374151;
--gray-800: #1f2937;
--gray-900: #111827;
--gray-950: #030712;
```

## Typography

### Font Stack
```css
--font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
--font-mono: ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace;
```

### Type Scale
```css
--text-xs: 0.75rem;     /* 12px */
--text-sm: 0.875rem;    /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.25rem;     /* 20px */
--text-2xl: 1.5rem;     /* 24px */
--text-3xl: 1.875rem;   /* 30px */
--text-4xl: 2.25rem;    /* 36px */
```

### Line Heights
```css
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

## Spacing System

```css
--space-0: 0;
--space-1: 0.25rem;     /* 4px */
--space-2: 0.5rem;      /* 8px */
--space-3: 0.75rem;     /* 12px */
--space-4: 1rem;        /* 16px */
--space-5: 1.25rem;     /* 20px */
--space-6: 1.5rem;      /* 24px */
--space-8: 2rem;        /* 32px */
--space-10: 2.5rem;     /* 40px */
--space-12: 3rem;       /* 48px */
--space-16: 4rem;       /* 64px */
--space-20: 5rem;       /* 80px */
```

## Border Radius

```css
--radius-sm: 0.125rem;   /* 2px */
--radius-md: 0.375rem;   /* 6px */
--radius-lg: 0.5rem;     /* 8px */
--radius-xl: 0.75rem;    /* 12px */
--radius-2xl: 1rem;      /* 16px */
--radius-full: 9999px;
```

## Shadows

```css
--shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
```

## Component Patterns

### Buttons

#### Primary Button
```css
.btn-primary {
  background: var(--primary-600);
  color: white;
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-lg);
  font-weight: 500;
  transition: all 0.2s;
}

.btn-primary:hover {
  background: var(--primary-700);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}
```

#### Secondary Button
```css
.btn-secondary {
  background: white;
  color: var(--gray-700);
  border: 1px solid var(--gray-300);
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-lg);
  font-weight: 500;
}
```

### Cards
```css
.card {
  background: white;
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--gray-200);
}
```

### Status Badges
```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 600;
}

.badge-success {
  background: var(--success-50);
  color: var(--success-600);
}

.badge-warning {
  background: var(--warning-50);
  color: var(--warning-600);
}

.badge-info {
  background: var(--info-50);
  color: var(--info-600);
}
```

### Form Controls
```css
.form-input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--gray-300);
  border-radius: var(--radius-lg);
  font-size: var(--text-base);
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px var(--primary-50);
}
```

## Layout System

### Container
```css
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

@media (min-width: 640px) {
  .container { padding: 0 var(--space-6); }
}

@media (min-width: 1024px) {
  .container { padding: 0 var(--space-8); }
}
```

### Grid
```css
.grid {
  display: grid;
  gap: var(--space-6);
}

.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
```

## Animations

```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

## Responsive Breakpoints

```css
/* Mobile First */
--screen-sm: 640px;   /* Small devices */
--screen-md: 768px;   /* Medium devices */
--screen-lg: 1024px;  /* Large devices */
--screen-xl: 1280px;  /* Extra large devices */
```

## Implementation Priority

1. **Phase 1**: Core design tokens (colors, typography, spacing)
2. **Phase 2**: Component styles (buttons, cards, forms)
3. **Phase 3**: Layout system and responsive grid
4. **Phase 4**: Animations and interactions
5. **Phase 5**: Dark mode support (future)