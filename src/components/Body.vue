<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <!-- Main Card -->
    <div
      class="w-full max-w-2xl bg-[#1e1e2e]/80 rounded-xl shadow-xl backdrop-blur-sm border border-white/10 overflow-hidden"
    >
      <!-- Header -->
      <div
        class="flex items-center gap-2 px-4 py-3 bg-[#2a2a3e] border-b border-white/10"
      >
        <div class="w-3 h-3 rounded-full bg-[#ff5f57]"></div>
        <div class="w-3 h-3 rounded-full bg-[#febc2e]"></div>
        <div class="w-3 h-3 rounded-full bg-[#28c840]"></div>
        <span class="ml-2 text-xs text-gray-400">info.js</span>
      </div>

      <!-- Content -->
      <div class="code-background p-6">
        <!-- Profile Section -->
        <div class="profile-section mb-8">
          <div class="flex items-center gap-6 mb-6">
            <!-- Avatar Container with Flame Effect -->
            <div class="relative">
              <div class="avatar-flame-container">
                <!-- Flame Effect -->
                <div class="avatar-wrapper">
                  <img
                    :src="
                      discordData?.data?.discord_user?.avatar
                        ? `https://cdn.discordapp.com/avatars/${discordId}/${discordData.data.discord_user.avatar}`
                        : '/default-avatar.png'
                    "
                    alt="Profile"
                    class="avatar-image"
                  />
                </div>
              </div>
              <!-- Status Indicator -->
              <div
                :class="[
                  'absolute -bottom-2 -right-2 w-4 h-4 rounded-full border-2 border-[#1e1e2e]',
                  statusColor,
                ]"
              ></div>
            </div>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2">
                <h1 class="text-2xl font-bold text-white">{{ discordName }}</h1>
                <!-- Custom Badges -->
                <div class="flex gap-1">
                  <div class="badge" title="Verified">
                    <i class="ri-verified-badge-fill text-blue-400"></i>
                  </div>
                  <div class="badge" title="Developer">
                    <i class="ri-code-s-slash-fill text-purple-400"></i>
                  </div>
                </div>
              </div>
              <p class="text-gray-400">{{ Bio }}</p>
              <!-- Discord Activity -->
              <div
                v-if="discordActivity"
                class="text-sm text-gray-400 flex items-center gap-2 mt-1"
              >
                <span class="text-purple-400">Playing:</span>
                {{ discordActivity.name }}
              </div>
              <!-- Social Links -->
              <div class="flex gap-3 mt-2">
                <a
                  v-for="link in socialLinks"
                  :key="link.name"
                  :href="link.url"
                  target="_blank"
                  class="text-white/60 hover:text-purple-400 transition-colors"
                >
                  <i :class="link.icon" class="text-xl"></i>
                </a>
              </div>
            </div>
          </div>

          <div class="w-full" :class="{ 'cursor-pointer': true }">
            <!-- Clickable Header -->
            <div
              @click="isOpen = !isOpen"
              class="flex items-center justify-between p-4 rounded-lg bg-gray-800/50 backdrop-blur-sm border border-white/10"
            >
              <!-- Left side with logo and name -->
              <div class="flex items-center gap-3">
                <div
                  class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center"
                >
                  <span class="text-white text-sm">L?</span>
                </div>
                <span class="text-white">Globlex Securities Co.Ltd</span>
              </div>

              <!-- Chevron icon -->
              <svg
                class="w-5 h-5 text-gray-400 transition-transform duration-200"
                :class="{ 'rotate-180': isOpen }"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </div>

            <!-- Dropdown Content -->
            <transition
              enter-active-class="transition duration-100 ease-out"
              enter-from-class="transform scale-95 opacity-0"
              enter-to-class="transform scale-100 opacity-100"
              leave-active-class="transition duration-75 ease-in"
              leave-from-class="transform scale-100 opacity-100"
              leave-to-class="transform scale-95 opacity-0"
            >
              <div
                v-show="isOpen"
                class="mt-2 p-4 rounded-lg bg-gray-800/50 backdrop-blur-sm border border-white/10"
              >
                <div class="flex flex-col space-y-2">
                  <a
                    v-for="social in socialLinks"
                    :key="social.name"
                    :href="social.url"
                    class="text-gray-300 hover:text-white flex items-center gap-2 p-2 rounded hover:bg-gray-700/50"
                  >
                    <i :class="social.icon"></i>
                    <span>{{ social.name }}</span>
                  </a>
                </div>
              </div>
            </transition>
          </div>

          <br />
          <hr />
          <br />

          <!-- Bio -->
          <div class="mb-6 p-4 rounded-xl bg-white/5 border border-white/10">
            <p class="text-gray-300 leading-relaxed">{{ Description }}</p>
          </div>

          <div
            class="w-full max-w-2xl bg-[#1e1e2e] rounded-xl shadow-2xl overflow-hidden"
          >
            <div class="code-background p-6">
              <div class="text-xl mb-4">
                <span class="text-green-400"><profile></span>
              </div>

              <div class="pl-4">
                <div class="code-line py-2">
                  <span class="text-blue-400">const </span>
                  <span class="text-yellow-400">developerInfo </span>
                  <span class="text-white">= </span>
                  <span class="text-purple-400">{</span>
                </div>
                <div class="code-line py-2 pl-4">
                  <span class="text-red-400">name</span>:
                  <span class="text-green-300">{{ Name }}</span
                  >,
                </div>
                <div class="code-line py-2 pl-4">
                  <span class="text-red-400">role</span>:
                  <span class="text-green-300">{{ role }}</span
                  >,
                </div>
                <div class="code-line py-2 pl-4">
                  <span class="text-red-400">skills</span>:
                  <span class="text-purple-400">[</span>
                  <span class="text-green-300">"React"</span>,
                  <span class="text-green-300">"Node.js"</span>,
                  <span class="text-green-300">"Python"</span>
                  <span class="text-purple-400">]</span>,
                </div>
                <div class="code-line py-2 pl-4">
                  <span class="text-red-400">contact</span>:
                  <span class="text-green-300"
                    >"goodplaceofficer@gmail.com"</span
                  >
                </div>
                <div class="code-line py-2">
                  <span class="text-purple-400">}</span>;
                </div>
              </div>

              <div class="text-xl mt-4">
                <span class="text-green-400"></profile></span>
                <span class="cursor-blink text-white">|</span>
              </div>
            </div>
          </div>
        </div>
        <!-- Payment Section -->
        <div class="payment-section mb-8">
          <div
            class="flex flex-col rounded-xl border border-white/10 p-4 backdrop-blur-sm bg-white/5"
          >
            <div class="payment-header">
              <h2 class="text-xl font-semibold text-white">Payment!</h2>
              <div
                class="h-px bg-gradient-to-r from-transparent via-white/20 to-transparent my-2"
              ></div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
              <!-- PayPal -->
              <div
                class="group relative text-sm hover:scale-[1.02] transition-all duration-300"
              >
                <div
                  class="relative flex items-center gap-x-4 px-4 py-3 rounded-xl border border-white/10 bg-white/5 before:absolute before:inset-0 before:rounded-xl before:p-[1px] before:bg-gradient-to-r before:from-transparent before:via-white/20 before:to-transparent hover:shadow-lg hover:shadow-white/10 transition-all duration-300"
                >
                  <div class="icon-wrapper">
                    <img
                      :src="paypalIcon"
                      class="z-20 h-12 w-12 rounded-xl bg-white/5 p-2.5 transition-all duration-300 group-hover:scale-110 shadow-lg shadow-purple-500/10 group-hover:shadow-purple-500/20 group-hover:bg-white/10"
                      alt="PayPal"
                    />
                  </div>
                  <div class="z-20 flex flex-col text-white">
                    <div class="font-medium flex items-center gap-2">
                      {{ paypalName }}
                      <button
                        @click="copyToClipboard(paypalName)"
                        class="hover:text-primary transition-colors"
                      >
                        <i class="ri-file-copy-line"></i>
                      </button>
                    </div>
                    <div
                      class="font-normal text-gray-400 flex items-center gap-2"
                    >
                      {{ paypalId }}
                      <button
                        @click="copyToClipboard(paypalId)"
                        class="hover:text-primary transition-colors"
                      >
                        <i class="ri-file-copy-line"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Truemoney -->
              <div
                class="group relative text-sm hover:scale-[1.02] transition-all duration-300"
              >
                <div
                  class="relative flex items-center gap-x-4 px-4 py-3 rounded-xl border border-white/10 bg-white/5 before:absolute before:inset-0 before:rounded-xl before:p-[1px] before:bg-gradient-to-r before:from-transparent before:via-white/20 before:to-transparent hover:shadow-lg hover:shadow-white/10 transition-all duration-300"
                >
                  <div class="icon-wrapper">
                    <img
                      :src="truemoneyIcon"
                      class="z-20 h-12 w-12 rounded-xl bg-white/5 p-2.5 transition-all duration-300 group-hover:scale-110 shadow-lg shadow-purple-500/10 group-hover:shadow-purple-500/20 group-hover:bg-white/10"
                      alt="Truemoney"
                    />
                  </div>
                  <div class="z-20 flex flex-col text-white">
                    <div class="font-medium flex items-center gap-2">
                      {{ truemoneyNumber }}
                      <button
                        @click="copyToClipboard(truemoneyNumber)"
                        class="hover:text-primary transition-colors"
                      >
                        <i class="ri-file-copy-line"></i>
                      </button>
                    </div>
                    <div
                      class="font-normal text-gray-400 flex items-center gap-2"
                    >
                      {{ truemoneyName }}
                      <button
                        @click="copyToClipboard(truemoneyName)"
                        class="hover:text-primary transition-colors"
                      >
                        <i class="ri-file-copy-line"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Projects Section -->
        <div class="projects-section">
          <div
            class="flex flex-col rounded-xl border border-white/10 p-4 backdrop-blur-sm bg-white/5"
          >
            <!-- Header -->
            <div class="payment-header text-center md:text-left">
              <h2 class="text-xl font-semibold text-white">Projects - Etc..</h2>
              <div
                class="h-px bg-gradient-to-r from-transparent via-white/20 to-transparent my-2"
              ></div>
            </div>

            <!-- Buttons -->
            <div
              class="flex flex-wrap gap-4 mt-4 justify-center md:justify-start"
            >
              <button
                @click="toggleShowProjects"
                class="glow-button px-4 py-2 rounded bg-white/10 hover:bg-white/20 transition-all duration-300 text-white relative overflow-hidden group w-full sm:w-auto"
              >
                <span class="relative z-10">
                  {{ showProjects ? "Hide" : "Show" }} Projects
                </span>
                <div class="glow-effect"></div>
              </button>
              <button
                @click="toggleUsed"
                class="glow-button px-4 py-2 rounded bg-white/10 hover:bg-white/20 transition-all duration-300 text-white relative overflow-hidden group w-full sm:w-auto"
              >
                <span class="relative z-10 text-white">
                  {{ used ? "Hide" : "Show" }} Tools
                </span>
                <div class="glow-effect"></div>
              </button>
              <button
                @click="toggleImages"
                class="glow-button px-4 py-2 rounded bg-white/10 hover:bg-white/20 transition-all duration-300 relative overflow-hidden group w-full sm:w-auto"
              >
                <span class="relative z-10 text-white">
                  {{ showImages ? "Hide" : "Show" }} Images
                </span>
                <div class="glow-effect"></div>
              </button>
              <button
                @click="toggleSkills"
                class="glow-button px-4 py-2 rounded bg-white/10 hover:bg-white/20 transition-all duration-300 relative overflow-hidden group w-full sm:w-auto"
              >
                <span class="relative z-10 text-white">
                  {{ showSkills ? "Hide" : "Show" }} Skills
                </span>
                <div class="glow-effect"></div>
              </button>
            </div>

            <transition
              name="fade"
              enter-active-class="transition ease-out duration-300"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-200"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div v-if="showSkills" class="mt-6 grid gap-6">
                <div
                  v-for="(skillList, category) in skills"
                  :key="category"
                  class="space-y-3"
                >
                  <h3 class="text-lg font-semibold text-white">
                    {{ category }}
                  </h3>
                  <div class="flex flex-wrap gap-2">
                    <div
                      v-for="skill in skillList"
                      :key="skill"
                      class="px-3 py-1 rounded-full bg-white/10 hover:bg-white/20 transition-all duration-300 cursor-pointer group relative"
                    >
                      <span class="text-white text-sm">{{ skill }}</span>
                      <div
                        class="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-all duration-300 rounded-full"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </transition>

            <transition
              name="fade"
              enter-active-class="transition ease-out duration-300"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-200"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div v-if="showImages" class="grid grid-cols-2 gap-4 mt-4">
                <div
                  v-for="(image, index) in images"
                  :key="index"
                  class="group relative rounded-lg overflow-hidden cursor-pointer"
                  @click="openImage(image)"
                >
                  <img
                    :src="image.url"
                    :alt="image.title"
                    class="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-110"
                  />
                  <div
                    class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center"
                  >
                    <p class="text-white font-medium">{{ image.title }}</p>
                  </div>
                </div>
              </div>
            </transition>

            <transition
              name="tools"
              enter-active-class="transition ease-out duration-300"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-200"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div v-if="used" class="mt-4 grid grid-cols-2 gap-4">
                <div
                  v-for="tool in tools"
                  :key="tool.id"
                  class="flex items-center gap-3 p-3 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-all duration-300 transform hover:scale-[1.02]"
                >
                  <i :class="tool.icon" class="text-2xl text-purple-400"></i>
                  <span class="text-white">{{ tool.name }}</span>
                </div>
              </div>
            </transition>

            <transition
              name="projects"
              enter-active-class="transition ease-out duration-300"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-200"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div v-if="showProjects" class="mt-4 grid grid-cols-1 gap-4">
                <div
                  v-for="repo in filteredRepos"
                  :key="repo.name"
                  class="p-4 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 transition-all duration-300"
                >
                  <div class="flex justify-between items-start">
                    <div>
                      <h3 class="text-lg font-medium text-white">
                        {{ repo.name }}
                      </h3>
                      <p class="text-gray-400 mt-2">
                        {{ repo.description || "No description available" }}
                      </p>
                    </div>
                    <a
                      :href="repo.html_url"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="text-white hover:text-purple-400 transition-colors duration-300"
                    >
                      <i class="ri-github-fill text-xl"></i>
                    </a>
                  </div>

                  <div class="mt-3 flex flex-wrap gap-2">
                    <span
                      v-if="repo.language"
                      class="px-3 py-1 rounded-full bg-white/10 text-white text-sm"
                    >
                      {{ repo.language }}
                    </span>
                    <span
                      class="px-3 py-1 rounded-full bg-white/10 text-white text-sm"
                    >
                      ⭐ {{ repo.stargazers_count }}
                    </span>
                    <span
                      class="px-3 py-1 rounded-full bg-white/10 text-white text-sm"
                    >
                      🍴 {{ repo.forks_count }}
                    </span>
                  </div>
                </div>
                <!-- Loading State -->
                <div
                  v-if="loading"
                  class="text-center text-white flex items-center justify-center gap-2"
                >
                  <svg
                    class="animate-spin h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    ></circle>
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Loading projects...
                </div>

                <!-- Error State -->
                <div
                  v-if="error"
                  class="text-center text-red-400 p-4 rounded-lg bg-red-500/10 border border-red-500/20"
                >
                  {{ error }}
                </div>
              </div>
            </transition>
          </div>
        </div>
        <div class="spotify-section mt-8">
          <div
            class="flex flex-col rounded-xl border border-white/10 p-4 backdrop-blur-sm bg-white/5"
          >
            <!-- Header -->
            <div class="spotify-header text-center md:text-left">
              <h2 class="text-xl font-semibold text-white">Spotify</h2>
              <div
                class="h-px bg-gradient-to-r from-transparent via-white/20 to-transparent my-2"
              ></div>
            </div>

            <!-- Spotify Embed -->
            <div
              class="mt-4 transform transition-all duration-300 hover:scale-[1.01]"
            >
              <iframe
                style="border-radius: 12px"
                src="https://open.spotify.com/embed/playlist/0tQKoL395qAwiOk1ZbqhTb?utm_source=generator"
                width="100%"
                height="152"
                frameBorder="0"
                allowfullscreen=""
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                loading="lazy"
              ></iframe>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <div
      v-show="showToast"
      class="fixed top-4 left-1/2 -translate-x-1/2 px-6 py-3 rounded-lg bg-white/10 backdrop-blur-sm text-white font-medium shadow-[0_0_15px_rgba(255,255,255,0.5)] transform transition-all duration-300 z-50"
      :class="{
        'translate-y-0 opacity-100': showToast,
        '-translate-y-full opacity-0': !showToast,
      }"
    >
      {{ toastMessage }}
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  name: "ProfileView",
  data() {
    return {
      Name: "Coey Stepthep",
      Bio: "Hiiiiiiiiiiii~!",
      Description: "My name's John",
      role: "Software Developer",
      skills: ["Vue.js", "React", "Node.js", "Python"],
      contact: "goodplaceofficer@gmail.com",

      isOpen: false,
      socialLinks: [
        {
          name: "GitHub",
          url: "https://github.com/eieiodenonetapallplayer/",
          icon: "ri-github-fill",
        },
        {
          name: "Website Store",
          url: "https://goodplace.rexzy.xyz/",
          icon: "ri-code-fill",
        },
        {
          name: "Carrent",
          url: "https://carsrent-beta.vercel.app/",
          icon: "ri-code-fill",
        },
        {
          name: "Broker",
          url: "https://www.globlex.co.th/",
          icon: "ri-code-fill",
        },
      ],

      images: [
        {
          url: "https://i.postimg.cc/1RgCYYCq/split-0-0.png",
          title: "Project 1",
        },
        {
          url: "https://i.postimg.cc/8kqK8B9n/split-1-0.png",
          title: "Project 2",
        },
        {
          url: "https://i.postimg.cc/ncBdn9tV/split-0-1.png",
          title: "Project 3",
        },
        {
          url: "https://i.postimg.cc/qvGj3fR9/split-1-1.png",
          title: "Project 4",
        },
      ],
      selectedImage: null,

      discordData: null,
      discordId: "1061613918641995796",
      loading: true,
      error: null,
      showImages: false,
      showSkills: false,
      skills: {
        Web: [
          "Vue.js",
          "Nuxt.js",
          "Node.js",
          "React.js",
          "TypeScript",
          "JavaScript",
          "CSS",
          "HTML",
        ],
        Programming: [
          "Python",
          "PyTorch",
          "C",
          "C++",
          "C#",
          "R",
          "MySQL",
          "PostgreSQL",
        ],
        Tools: ["VSCode", "Vim", "Git", "Linux", "Docker", "Nginx"],
        Design: ["Figma", "Photoshop", "Illustrator"],
        Other: ["Markdown", "LaTeX"],
      },

      // Payment Data
      paypalIcon: "https://i.postimg.cc/nLynnzB2/image.png",
      paypalName: "1KfVZ...",
      paypalId: "bc1qw508d..",
      truemoneyIcon: "https://i.postimg.cc/3rcZZLHx/truemoney.png",
      truemoneyNumber: "0979988416",
      truemoneyName: "รามิล ส...",

      // GitHub and Projects Data
      GITHUB_API_URL:
        "https://api.github.com/users/eieiodenonetapallplayer/repos",
      showProjects: false,
      used: false,
      loading: false,
      error: null,
      repositories: [],
      allowedProjects: [
        "Website-Goodplace",
        "Discord-RAT-2.0",
        "AllHackingTools",
        "Bot-boost",
        "discord-api-typescript",
        "discord-username-scraper",
        "Multi-tool-",
        "DiscordBot-RandomGif",
        "instagram-scraper",
        "Verificador-URL",
      ],
      tools: [
        { id: 1, name: "Discord PTB", icon: "ri-discord-line" },
        { id: 2, name: "Visual Studio Code", icon: "ri-code-line" },
        { id: 3, name: "Atom / Vim", icon: "ri-window-line" },
        { id: 4, name: "Firefox Nightly", icon: "ri-firefox-line" },
      ],

      // Toast Notification
      showToast: false,
      toastMessage: "",
      toastTimeout: null,

      // Theme and UI States
      isDarkMode: true,
      isMobile: false,
      isMenuOpen: false,
    };
  },

  computed: {
    filteredRepos() {
      return this.repositories
        .filter((repo) => this.allowedProjects.includes(repo.name))
        .sort((a, b) => b.stargazers_count - a.stargazers_count);
    },

    userAvatar() {
      const user = this.discordData?.data?.discord_user;
      if (!user) return "/default-avatar.png";

      if (user.avatar_decoration_data) {
        return `https://cdn.discordapp.com/avatar-decorations/${this.discordId}/${user.avatar_decoration_data.asset}`;
      }

      if (user.avatar) {
        return `https://cdn.discordapp.com/avatars/${this.discordId}/${user.avatar}?size=512`;
      }

      return "/default-avatar.png";
    },

    avatarDecorationStyle() {
      const decoration =
        this.discordData?.data?.discord_user?.avatar_decoration_data;
      if (!decoration) return {};

      return {
        "--avatar-decoration": `url(${decoration.asset})`,
        "--decoration-offset": decoration.offset || "0px",
      };
    },

    isPremium() {
      return this.discordData?.data?.discord_user?.premium_type > 0;
    },

    userBanner() {
      const user = this.discordData?.data?.discord_user;
      if (!user?.banner) return null;
      return `https://cdn.discordapp.com/banners/${this.discordId}/${user.banner}?size=1024`;
    },

    discordStatus() {
      if (!this.discordData) return "offline";
      return this.discordData.data.discord_status;
    },
    discordActivity() {
      if (!this.discordData?.data?.activities?.[0]) return null;
      return this.discordData.data.activities[0];
    },

    discordName() {
      return (
        this.discordData?.data?.discord_user?.global_name ||
        this.discordData?.data?.discord_user?.username ||
        "Loading..."
      );
    },

    statusColor() {
      const colors = {
        online: "bg-green-500",
        idle: "bg-yellow-500",
        dnd: "bg-red-500",
        offline: "bg-gray-500",
      };
      return colors[this.discordStatus] || colors.offline;
    },
  },

  methods: {
    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },
    async fetchGithubRepos() {
      this.loading = true;
      this.error = null;
      try {
        const cache = localStorage.getItem("github_repos");
        if (cache) {
          this.repositories = JSON.parse(cache);
          this.loading = false;
          return;
        }
        const response = await fetch(this.GITHUB_API_URL);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.repositories = data;
        localStorage.setItem("github_repos", JSON.stringify(data));
      } catch (err) {
        this.error =
          "Error loading GitHub repositories. Please mentors try again later.";
        console.error("Error:", err);
      } finally {
        this.loading = false;
      }
    },

    toggleSkills() {
      this.showSkills = !this.showSkills;
    },

    toggleImages() {
      this.showImages = !this.showImages;
    },
    openImage(image) {
      this.selectedImage = image;
    },

    async fetchDiscordData() {
      try {
        this.loading = true;
        const response = await fetch(
          `https://api.lanyard.rest/v1/users/${this.discordId}`
        );
        const data = await response.json();
        this.discordData = data;
      } catch (err) {
        this.error = "Failed to fetch Discord data";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    initWebSocket() {
      this.ws = new WebSocket("wss://api.lanyard.rest/socket");

      this.ws.onopen = () => {
        this.ws.send(
          JSON.stringify({
            op: 2,
            d: {
              subscribe_to_id: this.discordId,
            },
          })
        );
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.op === 1) {
          this.ws.send(
            JSON.stringify({
              op: 3,
            })
          );
        }

        if (data.op === 0 && data.t === "PRESENCE_UPDATE") {
          this.discordData = {
            data: data.d,
          };
        }
      };

      this.ws.onclose = () => {
        if (this.wsRetries < this.maxRetries) {
          this.retryTimeout = setTimeout(() => {
            this.wsRetries++;
            this.initWebSocket();
          }, 3000);
        }
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket Error:", error);
      };
    },

    closeWebSocket() {
      if (this.ws) {
        this.ws.close();
      }
      if (this.retryTimeout) {
        clearTimeout(this.retryTimeout);
      }
    },

    toggleShowProjects() {
      this.showProjects = !this.showProjects;
      if (this.showProjects && this.repositories.length === 0) {
        this.fetchGithubRepos();
      }
    },

    toggleUsed() {
      this.used = !this.used;
    },

    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      document.documentElement.classList.toggle("dark");
    },

    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },

    async copyToClipboard(text) {
      try {
        await navigator.clipboard.writeText(text);
        this.showToastMessage("Copied to clipboard!");
      } catch (err) {
        this.showToastMessage("Failed to copy!");
        console.error("Failed to copy:", err);
      }
    },

    showToastMessage(message, duration = 3000) {
      if (this.toastTimeout) {
        clearTimeout(this.toastTimeout);
      }

      this.toastMessage = message;
      this.showToast = true;

      this.toastTimeout = setTimeout(() => {
        this.showToast = false;
        this.toastMessage = "";
      }, duration);
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },

    getLanguageColor(language) {
      const colors = {
        JavaScript: "#f1e05a",
        Python: "#3572A5",
        HTML: "#e34c26",
        CSS: "#563d7c",
        Vue: "#41b883",
      };
      return colors[language] || "#858585";
    },

    checkMobile() {
      this.isMobile = window.innerWidth < 768;
    },

    openExternalLink(url) {
      window.open(url, "_blank", "noopener noreferrer");
    },
  },

  watch: {
    repositories: {
      handler(newRepos) {
        if (newRepos.length > 0) {
          this.error = null;
        }
      },
      deep: true,
    },
  },

  mounted() {
    this.checkMobile();
    this.fetchDiscordData();
    this.initWebSocket();
    setInterval(this.fetchDiscordData, 30000);
    window.addEventListener("resize", this.checkMobile);

    if (
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    ) {
      this.isDarkMode = true;
      document.documentElement.classList.add("dark");
    }
  },

  beforeUnmount() {
    this.closeWebSocket();
    window.removeEventListener("resize", this.checkMobile);
    if (this.toastTimeout) {
      clearTimeout(this.toastTimeout);
    }
  },
};
</script>

<style scoped>
/* Global Styles */
body {
  background-color: #1e1e2e;
  color: #e0e0e0;
  font-family: "Courier New", monospace;
}

/* Base Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Code Background */
.code-background {
  background-color: #1e1e2e;
  font-family: "JetBrains Mono", monospace;
}

.code-line {
  transition: all 0.3s ease;
}
.code-line:hover {
  background-color: #3a3a5a;
  transform: translateX(10px);
}
.cursor-blink {
  animation: blink 1s infinite;
}
@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

/* Glow Effect */
.glow-hr {
  margin-top: 0.5rem;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    rgba(147, 51, 234, 0.5)
  );
}
.glow-button {
  position: relative;
}
.glow-button .glow-effect {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    45deg,
    rgba(147, 51, 234, 0.5),
    rgba(236, 72, 153, 0.5),
    rgba(59, 130, 246, 0.5)
  );
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 0;
}
.glow-button:hover .glow-effect {
  opacity: 1;
}

/* Avatar Flame Effect */
.avatar-flame-container {
  position: relative;
  width: 80px;
  height: 80px;
}
.avatar-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 0 15px rgba(147, 51, 234, 0.5);
}
.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.avatar-flame-container::before {
  content: '';
  position: absolute;
  inset: -10px;
  background: radial-gradient(
    circle,
    rgba(147, 51, 234, 0.3) 0%,
    transparent 70%
  );
  animation: flamePulse 2s ease-in-out infinite;
}
@keyframes flamePulse {
  0% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 0.5;
  }
}
</style>