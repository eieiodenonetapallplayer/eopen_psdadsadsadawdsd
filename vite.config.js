import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5137, // เปลี่ยนเป็น 3000 หรือพอร์ตอื่น
    proxy: {
      '/run-python': {
        target: 'http://localhost:5137',
        changeOrigin: true
      }
    }
  }
});