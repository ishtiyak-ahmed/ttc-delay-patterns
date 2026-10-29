export const fmt = (n: number) => new Intl.NumberFormat('en-CA').format(n)
export const percent = (n: number, d: number) => 100 * n / d
