<template>
  <div id="app" class="relative min-h-screen bg-[#1e1e2e] text-white">
    <!-- Loading Screen -->
    <div v-if="isLoading" class="fixed inset-0 flex items-center justify-center bg-[#1e1e2e] z-50">
      <div class="text-2xl animate-pulse">Loading...</div>
    </div>

    <!-- Snow Effects -->
    <Snowf 
      :amount="100" 
      :size="5" 
      :speed="1.5" 
      :wind="2" 
      :color="'#fff'" 
      :opacity="0.8" 
      :swing="1" 
      :z-index="5" 
    />
    <SnowRGB 
      :amount="100" 
      :size="5" 
      :speed="1.5" 
      :wind="2" 
      :opacity="0.8" 
      :swing="1" 
      :z-index="5" 
      :rgb-mode="true" 
      :glow-intensity="0.5" 
    />

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-8">
      <!-- Python Runner Section -->
      <section class="mb-12 text-center">
        <h2 class="text-3xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent">
          Run Python Script
        </h2>
        <button
          @click="runPythonScript"
          class="glow-button px-8 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 text-xl font-semibold hover:from-purple-700 hover:to-pink-700 transition-all duration-300 relative overflow-hidden shadow-lg hover:shadow-2xl transform hover:scale-105"
        >
          <span class="relative z-10">Run main.py</span>
          <div class="glow-effect absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
        </button>
        <div
          id="python-output"
          class="mt-6 p-4 bg-gray-800/80 rounded-xl border border-white/10 text-left font-mono text-sm max-h-96 overflow-y-auto"
          v-html="pythonOutput"
        ></div>
      </section>

      <!-- Other Components -->
      <Header />
      <Body />
      <Footer />

      <!-- Floating Icons -->
      <div class="fixed inset-0 pointer-events-none z-10">
        <div v-for="(icon, index) in floatingIcons" :key="index" 
             :style="icon.style" 
             class="absolute text-2xl animate-float">
          {{ icon.icon }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import Snowf from './components/Snowf.vue';
import SnowRGB from './components/SnowRGB.vue';
import Body from './components/Body.vue';

const isLoading = ref(true);
const pythonOutput = ref('');
const floatingIcons = ref([
  { icon: '❄', style: { top: '10%', left: '20%', animationDuration: '5s' } },
  { icon: '✨', style: { top: '30%', left: '80%', animationDuration: '7s' } },
  { icon: '🌙', style: { top: '50%', left: '10%', animationDuration: '6s' } },
  { icon: '🌹', style: { top: '70%', left: '90%', animationDuration: '8s' } },
]);

async function runPythonScript() {
  pythonOutput.value = 'Running script...';
  try {
    const response = await fetch('/run-python', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    const data = await response.text();
    pythonOutput.value = data.replace(/\n/g, '<br>'); // แปลง newline เป็น <br> สำหรับ HTML
  } catch (error) {
    pythonOutput.value = `Error: ${error.message}`;
  }
}

onMounted(() => {
  setTimeout(() => {
    isLoading.value = false;
  }, 3000);
});
</script>

<style scoped>
.glow-button {
  position: relative;
}
.glow-button .glow-effect {
  transition: opacity 0.3s ease;
}
.animate-float {
  animation: float linear infinite;
}
@keyframes float {
  0% { transform: translateY(0); opacity: 1; }
  50% { opacity: 0.5; }
  100% { transform: translateY(-100vh); opacity: 0; }
}
</style>