/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx,svelte}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['roboto', 'sans-serif'],
        serif: ['roboto', 'serif'],
      },
      colors: {
        background: '#121212',
        card: '#1A1A1A',
        accent: '#FFD700',
      },
    },
  },
  plugins: [],
};