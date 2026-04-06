/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        brand: { 500: '#00e5ff', 600: '#00b8d4' },
        dark:  { 900: '#080c14', 800: '#0e1520', 700: '#141d2e' }
      }
    }
  },
  plugins: []
}