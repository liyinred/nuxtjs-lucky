<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-4 sm:py-6 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
          <div class="flex flex-col sm:flex-row items-start sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
            <img src="/portal/logo.png" class="h-16 sm:h-20 w-auto" />
            <div>
              <h1 class="text-xl sm:text-3xl font-bold text-gray-900">
                MSBIO Lab Portal
              </h1>
              <p class="mt-1 text-xs sm:text-sm text-gray-500">
                Laboratory L02 - Documents and Tools
              </p>
            </div>
          </div>
          <div class="w-full md:w-auto">
            <span v-if="isAuthenticated"
              class="inline-flex flex-col sm:flex-row items-start sm:items-center gap-3 sm:gap-5">
              <span class="text-gray-700 dark:text-gray-300 text-base sm:text-lg font-medium tracking-wide">
                👋 Welcome,
                <span class="text-indigo-600 dark:text-indigo-400">{{
                  username
                }}</span>
              </span>

              <button @click="logout"
                class="px-3 py-1 sm:px-4 sm:py-2 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg shadow-md hover:shadow-lg transition-all duration-300 hover:from-red-600 hover:to-red-700 transform hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-opacity-50 text-sm sm:text-base">
                Logout
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 inline ml-1" viewBox="0 0 20 20"
                  fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                    clip-rule="evenodd" />
                </svg>
              </button>
            </span>
          </div>
        </div>
      </div>
    </header>

    <!-- Login Form (shown when not authenticated) -->
    <div v-if="!isAuthenticated" class="w-[90%] sm:max-w-md mx-auto mt-16 p-8 bg-white rounded-lg shadow-md">
      <h2 class="text-2xl font-bold text-center mb-6">Login to MSBIO Portal</h2>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
          <input v-model="loginForm.username" type="text" id="username" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input v-model="loginForm.password" type="password" id="password" required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
        </div>
        <div>
          <button type="submit"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Login
          </button>
        </div>
      </form>
    </div>

    <!-- Main Content -->
    <main v-if="isAuthenticated" class="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <!-- Search and Filter -->
      <div class="mb-8 flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
        <div class="relative w-full sm:w-64">
          <input type="text" placeholder="Search documents..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            v-model="searchQuery" />
          <div class="absolute left-3 top-2.5 text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
        <div class="flex space-x-2">
          <button v-for="category in categories" :key="category" @click="toggleCategory(category)" :class="{
            'bg-blue-100 text-blue-800':
              selectedCategories.includes(category),
            'bg-gray-100 text-gray-800':
              !selectedCategories.includes(category),
          }" class="px-3 py-1 text-sm rounded-full hover:bg-gray-200 transition-colors">
            {{ category }}
          </button>
        </div>
      </div>

      <!-- Documents Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <a v-for="document in filteredDocuments" :key="document.id" :href="document.image" target="_blank"
          rel="noopener noreferrer"
          class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow block no-underline"
          @click="handleCardClick(document, $event)">
          <div class="h-48 bg-gray-100 flex items-center justify-center p-4">
            <img :src="document.image" :alt="document.title" class="max-h-full max-w-full object-contain" />
          </div>
          <div class="p-4">
            <h3 class="font-medium text-gray-900 mb-1">{{ document.title }}</h3>
            <div class="flex justify-between items-center text-sm">
              <span
                class="px-3 py-1 bg-gradient-to-r from-blue-200 to-blue-500 text-white rounded-full font-medium shadow-sm">
                {{ document.category }}
              </span>
              <span class="text-gray-500 font-medium italic">
                {{ formatUpdatedDate(document.date) }}
              </span>
            </div>
          </div>
        </a>
      </div>

      <!-- Markdown Modal -->
      <transition enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 transform -translate-y-4" enter-to-class="opacity-100 transform translate-y-0"
        leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 transform translate-y-0"
        leave-to-class="opacity-0 transform -translate-y-4">
        <div v-if="showMarkdownModal" @click.self="closeModal"
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <transition enter-active-class="transition-all duration-300 ease-out"
            enter-from-class="opacity-0 transform scale-95" enter-to-class="opacity-100 transform scale-100"
            leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 transform scale-100"
            leave-to-class="opacity-0 transform scale-95">
            <div class="bg-white rounded-lg shadow-xl max-w-[90vw] md:max-w-[65vw] w-full max-h-[90vh] flex flex-col">
              <div class="p-4 border-b flex justify-between items-center">
                <div class="text-xl italic font-medium text-gray-600">
                  {{ currentMarkdownTitle }}
                </div>
                <button @click="showMarkdownModal = false" class="text-gray-500 hover:text-gray-700">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div class="p-4 overflow-y-auto flex-1 markdown-body" v-html="renderedMarkdown"></div>
            </div>
          </transition>
        </div>
      </transition>

      <!-- Chemistry Tools Modal -->
      <transition enter-active-class="transition-opacity duration-300 ease-out" enter-from-class="opacity-0"
        enter-to-class="opacity-100" leave-active-class="transition-opacity duration-200 ease-in"
        leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div v-if="showChemistryModal" @click.self="closeModal"
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div class="bg-white rounded-lg shadow-xl max-w-[90vw] md:max-w-[60vw] w-full max-h-[90vh] overflow-auto">
            <div class="p-4">
              <div class="flex justify-between items-center mb-6">
                <div class="text-xl italic font-medium text-gray-600">
                  BioMolecular
                </div>
                <button @click="showChemistryModal = false" class="text-gray-500 hover:text-gray-700">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div class="flex flex-col gap-5">
                <!-- Molarity Calculator -->
                <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <h3 class="font-medium text-lg mb-3 text-gray-800">
                    Molarity Calculator
                  </h3>
                  <div class="space-y-4">
                    <div class="bg-white p-10 rounded-lg shadow-sm">
                      <!-- 使用flex-wrap实现自动换行 -->
                      <div class="flex flex-wrap items-center justify-center gap-2 mb-4">
                        <!-- Mass 输入框 -->
                        <div class="flex items-center">
                          <input v-model.number="mass" type="number"
                            class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Mass" />
                          <select v-model="massUnit"
                            class="ml-2 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="kg">kg</option>
                            <option value="g">g</option>
                            <option value="mg">mg</option>
                          </select>
                        </div>

                        <!-- 等号 -->
                        <span class="mx-2 text-gray-600 font-bold">=</span>

                        <!-- Concentration 输入框 -->
                        <div class="flex items-center">
                          <input v-model.number="concentration" type="number"
                            class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Conc." />
                          <select v-model="concentrationUnit"
                            class="ml-2 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="M">M</option>
                            <option value="mM">mM</option>
                            <option value="μM">μM</option>
                            <option value="nM">nM</option>
                            <option value="pM">pM</option>
                            <option value="fM">fM</option>
                          </select>
                        </div>

                        <!-- 乘号 -->
                        <span class="mx-2 text-gray-600 font-bold">×</span>

                        <!-- Volume 输入框 -->
                        <div class="flex items-center">
                          <input v-model.number="volume" type="number"
                            class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Volume" />
                          <select v-model="volumeUnit"
                            class="ml-2 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="L">L</option>
                            <option value="mL">mL</option>
                            <option value="μL">μL</option>
                          </select>
                        </div>

                        <!-- 乘号 -->
                        <span class="mx-2 text-gray-600 font-bold">×</span>

                        <!-- Molecular Weight 输入框 -->
                        <div class="flex items-center">
                          <input v-model.number="molecularWeight" type="number"
                            class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="MW" />
                          <span class="ml-2 text-gray-600">g/mol</span>
                        </div>
                      </div>

                      <!-- 按钮区域 -->
                      <div class="flex flex-wrap justify-end gap-4 mt-6">
                        <button @click="reset1"
                          class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400">
                          Reset
                        </button>
                        <button @click="calculate"
                          class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400">
                          Calculate
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Molecular Weight Calculator -->
                <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <h3 class="font-medium text-lg mb-3 text-gray-800">
                    Molecular Weight Calculator
                  </h3>
                  <div class="space-y-4">
                    <div class="bg-white p-4 md:p-10 rounded-lg shadow-sm max-w-full overflow-hidden">
                      <!-- 第一行：输入框和Calculate按钮 -->
                      <div class="flex flex-wrap gap-2 mb-4 w-full">
                        <input v-model="molecularFormula" type="text"
                          placeholder="Please enter the molecular formula (e.g., H2O)"
                          class="min-w-[150px] flex-grow px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
                        <button @click="massCalculator"
                          class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 whitespace-nowrap">
                          Calculate
                        </button>
                      </div>

                      <!-- 第二行：总分子量显示 -->
                      <div class="flex flex-wrap gap-2 items-center w-full">
                        <label class="text-gray-700 whitespace-nowrap">Total molecular weight:</label>
                        <input :value="totalMass" readonly
                          class="px-3 py-2 border border-gray-300 rounded-md bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 w-[100px] min-w-[100px]" />
                        <span class="text-gray-700 whitespace-nowrap">g/mol</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Dilution Calculator -->
                <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <h3 class="font-medium text-lg mb-3 text-gray-800">
                    Dilution Calculator
                  </h3>
                  <div class="space-y-4">
                    <div class="bg-white p-10 rounded-lg shadow-sm">
                      <div class="flex flex-wrap items-center justify-center gap-2 mb-4">
                        <!-- 初始溶液 - 现在作为一个可换行的单元 -->
                        <div class="flex flex-wrap items-center justify-center gap-2">
                          <div class="flex items-center">
                            <input v-model.number="c1" type="number"
                              class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                              placeholder="C1" />
                            <select v-model="c1Unit"
                              class="ml-2 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                              <option value="M">M</option>
                              <option value="mM">mM</option>
                              <option value="μM">μM</option>
                              <option value="nM">nM</option>
                              <option value="pM">pM</option>
                              <option value="fM">fM</option>
                            </select>
                          </div>

                          <span class="text-gray-600 font-bold">×</span>

                          <div class="flex items-center">
                            <input v-model.number="v1" type="number"
                              class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                              placeholder="V1" />
                            <select v-model="v1Unit"
                              class="ml-2 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                              <option value="L">L</option>
                              <option value="mL">mL</option>
                              <option value="μL">μL</option>
                            </select>
                          </div>
                        </div>

                        <!-- 等号 -->
                        <div class="flex justify-center">
                          <span class="text-gray-600 font-bold">=</span>
                        </div>

                        <!-- 稀释后溶液 - 现在作为一个可换行的单元 -->
                        <div class="flex flex-wrap items-center justify-center gap-2">
                          <div class="flex items-center">
                            <input v-model.number="c2" type="number"
                              class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                              placeholder="C2" />
                            <select v-model="c2Unit"
                              class="ml-2 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                              <option value="M">M</option>
                              <option value="mM">mM</option>
                              <option value="μM">μM</option>
                              <option value="nM">nM</option>
                              <option value="pM">pM</option>
                              <option value="fM">fM</option>
                            </select>
                          </div>

                          <span class="text-gray-600 font-bold">×</span>

                          <div class="flex items-center">
                            <input v-model.number="v2" type="number"
                              class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                              placeholder="V2" />
                            <select v-model="v2Unit"
                              class="ml-2 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                              <option value="L">L</option>
                              <option value="mL">mL</option>
                              <option value="μL">μL</option>
                            </select>
                          </div>
                        </div>
                      </div>

                      <!-- 按钮区域 -->
                      <div class="flex justify-end gap-4 mt-6">
                        <button @click="reset2"
                          class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400">
                          Reset
                        </button>
                        <button @click="dilution_calculate"
                          class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400">
                          Calculate
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- Empty State -->
      <div v-if="filteredDocuments.length === 0" class="text-center py-12">
        <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24"
          stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="mt-2 text-lg font-medium text-gray-900">
          No documents found
        </h3>
        <p class="mt-1 text-gray-500">
          Try adjusting your search or filter criteria.
        </p>
      </div>

      <!-- Future Expansion Notice -->
      <div class="mt-12 p-6 bg-blue-50 rounded-lg border border-blue-200">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-400" viewBox="0 0 20 20"
              fill="currentColor">
              <path fill-rule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2h-1V9z"
                clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-blue-800">Future Expansion</h3>
            <div class="mt-2 text-sm text-blue-700">
              <p>
                This portal will be expanded to include additional lab
                documents, equipment status monitoring, and team communication
                features.
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import Swal from "sweetalert2";
import MarkdownIt from "markdown-it";
import mk from "@traptitech/markdown-it-katex";
import "katex/dist/katex.min.css";

useHead({
  title: "MSBIO Portal",
});

const loginForm = ref({
  username: "",
  password: "",
});

const isAuthenticated = ref(false);
const username = ref("");
const role = ref("");

// 从 JWT token 解码 payload
const decodeJwtPayload = (token) => {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const payload = JSON.parse(atob(base64));
    console.log(payload, Date.now());
    return payload;
  } catch (error) {
    console.error("Failed to decode JWT:", error);
    return null;
  }
};

// 检查认证状态
const checkAuth = () => {
  const token = localStorage.getItem("jwt_token");
  console.log("JWT: ", token);

  if (token) {
    const payload = decodeJwtPayload(token);

    if (payload && payload.exp * 1000 > Date.now()) {
      isAuthenticated.value = true;
      // 从 payload 中提取 sub 和 role
      username.value = payload.sub || "";
      role.value = payload.role || "";

      fetchDocuments();
    } else {
      localStorage.removeItem("jwt_token");
      username.value = "";
      role.value = "";

      Swal.fire({
        icon: "warning",
        title: "Session Expired",
        text: "Your session has timed out. Please login again.",
        confirmButtonText: "OK",
      });
    }
  }
};

// 页面加载时检查认证状态
onMounted(() => {
  checkAuth();
});

const handleLogin = async () => {
  try {
    const response = await fetch("http://localhost:8082/login_portal", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(loginForm.value),
    });

    if (!response.ok) {
      throw new Error("Login failed");
    }

    const data = await response.json();
    localStorage.setItem("jwt_token", data.access_token);

    // 解码 token 并设置用户信息
    const payload = decodeJwtPayload(data.access_token);
    if (payload) {
      username.value = payload.sub || "";
      role.value = payload.role || "";
    }
    isAuthenticated.value = true;

    await fetchDocuments();

    Swal.fire({
      icon: "success",
      title: "Login Successful",
      showConfirmButton: false,
      timer: 1500,
    });

  } catch (error) {
    Swal.fire({
      icon: "error",
      title: "Login Failed",
      text: "Invalid username or password",
    });
  }
};

const logout = () => {
  localStorage.removeItem("jwt_token");
  isAuthenticated.value = false;
  loginForm.value = { username: "", password: "" };

  Swal.fire({
    title: "Logged Out",
    text: "You have been successfully logged out.",
    icon: "success",
    confirmButtonText: "OK",
  });
};

const documents = ref([]);

// const fetchDocuments = async () => {
//   try {
//     const response = await fetch("http://localhost:8082/api/public/portal/json/documents.json");
//     if (!response.ok) {
//       throw new Error("Network response was not ok");
//     }
//     documents.value = await response.json();
//   } catch (error) {
//     console.error("Error fetching documents:", error);
//   }
// };

const fetchDocuments = async () => {
  try {
    const token = localStorage.getItem("jwt_token");
    if (!token) {
      isAuthenticated.value = false;
      username.value = "";
      role.value = "";
      throw new Error("No JWT token found");
    }

    const response = await fetch(`http://localhost:8082/api_public/portal/json/documents.json?v=${new Date().getTime()}`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      localStorage.removeItem("jwt_token");
      isAuthenticated.value = false;
      username.value = "";
      role.value = "";
      throw new Error("Network response was not ok");
    }
    documents.value = await response.json();

  } catch (error) {

    console.error("Error fetching documents:", error);
    Swal.fire({
      icon: "error",
      title: "Authentication failed, please log in again",
      text: error.message,
    });

  }
};

// Calculate上海时间与给定日期的天数差
const formatUpdatedDate = (dateString) => {
  if (!dateString || isNaN(new Date(dateString))) {
    return "Invalid date";
  }

  try {
    // 获取上海时区的当前日期(00:00:00)
    const options = { timeZone: "Asia/Shanghai" };
    const todayStr = new Date().toLocaleDateString("en-US", options);
    const today = new Date(todayStr);

    // 解析输入日期并转换为上海时区日期
    const inputDate = new Date(dateString);
    const inputDateStr = inputDate.toLocaleDateString("en-US", options);
    const shanghaiInputDate = new Date(inputDateStr);

    // Calculate天数差
    const timeDiff = today - shanghaiInputDate;
    const dayDiff = Math.floor(timeDiff / (1000 * 60 * 60 * 24));

    if (dayDiff < 0) {
      return "Future date";
    } else if (dayDiff === 0) {
      return "Updated today";
    } else if (dayDiff === 1) {
      return "Updated 1 day ago";
    } else {
      return `Updated ${dayDiff} days ago`;
    }
  } catch (e) {
    console.error("Date formatting error:", e);
    return "Date error";
  }
};

const categories = ref(["All", "Cleaning", "Safety", "Schedule", "Tool"]);
const selectedCategories = ref(["All"]);
const searchQuery = ref("");
const showChemistryModal = ref(false);

const showMarkdownModal = ref(false);
const renderedMarkdown = ref("");
const currentMarkdownTitle = ref("");

const mass = ref(null);
const massUnit = ref("g");
const concentration = ref(null);
const concentrationUnit = ref("mM");
const volume = ref(null);
const volumeUnit = ref("mL");
const molecularWeight = ref(null);

const molecularFormula = ref("");
const totalMass = ref("");

const c1 = ref("");
const c2 = ref("");
const v1 = ref("");
const v2 = ref("");
const c1Unit = ref("mM");
const c2Unit = ref("mM");
const v1Unit = ref("mL");
const v2Unit = ref("mL");

const handleCardClick = async (document, event) => {
  if (document.category === "markdown") {
    event.preventDefault();
    currentMarkdownTitle.value = document.title;
    await loadAndRenderMarkdown(document.file);
    showMarkdownModal.value = true;
  } else if (document.title === "BioMolecular") {
    event.preventDefault();
    showChemistryModal.value = true;
  }
};

// const md = new MarkdownIt({
//   html: true,
//   linkify: true,
//   typographer: true,
//   breaks: true
// }).use(mk);

const md = new MarkdownIt({
  html: true, // 允许 HTML 标签（默认 false）
  linkify: true, // 自动识别文本中的链接并转换为 <a> 标签
  typographer: true, // 启用排版优化（如智能引号、破折号等）
  breaks: true, // 将换行符 `\n` 转换为 `<br>`（默认 false）
  xhtmlOut: true, // 使用 XHTML 风格的闭合标签（如 `<br />`）
  langPrefix: "language-", // 代码块的语言类名前缀（用于语法高亮）
  quotes: "“”‘’", // 设置智能引号的样式（typographer 启用时有效）
}).use(mk);

const loadAndRenderMarkdown = async (filePath) => {
  try {
    const response = await fetch(filePath);
    if (!response.ok) throw new Error("Markdown文件加载失败");

    const markdownText = await response.text();
    renderedMarkdown.value = md.render(markdownText);
  } catch (error) {
    console.error("加载Markdown失败:", error);
    renderedMarkdown.value = `<p>无法加载Markdown内容: ${error.message}</p>`;
  }
};

const closeModal = () => {
  showChemistryModal.value = false;
  showMarkdownModal.value = false;
};

function toggleCategory(category) {
  if (category === "All") {
    selectedCategories.value = ["All"];
  } else {
    if (selectedCategories.value.includes("All")) {
      selectedCategories.value = selectedCategories.value.filter(
        (c) => c !== "All"
      );
    }

    const index = selectedCategories.value.indexOf(category);
    if (index > -1) {
      selectedCategories.value.splice(index, 1);

      if (selectedCategories.value.length === 0) {
        selectedCategories.value = ["All"];
      }
    } else {
      selectedCategories.value.push(category);
    }
  }
}

const filteredDocuments = computed(() => {
  return documents.value.filter((doc) => {
    if (role.value === "user" && doc.category === "Tool") {
      return false;
    }
    const categoryMatch =
      selectedCategories.value.includes("All") ||
      selectedCategories.value.includes(doc.category);

    const searchMatch =
      doc.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      doc.category.toLowerCase().includes(searchQuery.value.toLowerCase());

    return categoryMatch && searchMatch;
  });
});

const calculate = async () => {
  // Check if molecularWeight is filled
  if (!molecularWeight.value) {
    await Swal.fire({
      icon: "warning",
      title: "Missing Input",
      text: "Molecular Weight is required!",
    });
    return;
  }

  // Count how many of the other values are filled
  const filledValues = [mass.value, concentration.value, volume.value].filter(
    (val) => val !== null && val !== ""
  ).length;

  // Check if exactly two of the other values are filled
  if (filledValues !== 2) {
    await Swal.fire({
      icon: "error",
      title: "Invalid Input",
      text: "Please fill exactly two of Mass, Concentration, or Volume fields!",
    });
    return;
  }

  try {
    const postData = {
      massValue: mass.value === "" ? null : mass.value,
      massUnit: massUnit.value === "" ? null : massUnit.value,
      concentrationValue:
        concentration.value === "" ? null : concentration.value,
      concentrationUnit:
        concentrationUnit.value === "" ? null : concentrationUnit.value,
      volumeValue: volume.value === "" ? null : volume.value,
      volumeUnit: volumeUnit.value === "" ? null : volumeUnit.value,
      molecularWeight:
        molecularWeight.value === "" ? null : molecularWeight.value,
    };

    const response = await fetch("http://localhost:8082/molarity_calculator", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postData),
    });

    const data = await response.json();

    // Fill the empty field with the calculated value
    if (mass.value === null || mass.value === "") {
      mass.value = data.calculatedValue;
      massUnit.value = data.calculatedUnit;
    } else if (concentration.value === null || concentration.value === "") {
      concentration.value = data.calculatedValue;
      concentrationUnit.value = data.calculatedUnit;
    } else if (volume.value === null || volume.value === "") {
      volume.value = data.calculatedValue;
      volumeUnit.value = data.calculatedUnit;
    }

    // Show success message
    await Swal.fire({
      icon: "success",
      title: "Calculation Complete",
      text: `${data.message}: ${data.calculatedValue} ${data.calculatedUnit}`,
      showConfirmButton: true,
    });
  } catch (error) {
    console.error("Error:", error);
    await Swal.fire({
      icon: "error",
      title: "Error",
      text: "An error occurred during calculation",
      footer: error.message,
    });
  }
};

const reset1 = () => {
  mass.value = null;
  massUnit.value = "g";
  concentration.value = null;
  concentrationUnit.value = "mM";
  volume.value = null;
  volumeUnit.value = "mL";
  molecularWeight.value = null;
};

const reset2 = () => {
  c1.value = "";
  v1.value = "";
  c2.value = "";
  v2.value = "";
  c1Unit.value = "M";
  v1Unit.value = "mL";
  c2Unit.value = "mM";
  v2Unit.value = "mL";
};

// 检查是否有且仅有一个空值
const checkEmptyFields = () => {
  const fields = [c1.value, v1.value, c2.value, v2.value];
  const emptyCount = fields.filter((value) => value === "").length;

  if (emptyCount === 0) {
    Swal.fire({
      icon: "warning",
      title: "No Calculation Needed",
      text: "All fields are filled. Please clear one field to perform the calculation",
    });
    return false;
  }

  if (emptyCount > 1) {
    Swal.fire({
      icon: "error",
      title: "Error",
      text: "Exactly one field must be empty to perform the calculation",
    });
    return false;
  }

  return true;
};

// 转换空字符串为null
const convertEmptyToNull = (value) => {
  return value === "" ? null : Number(value);
};

// Calculate函数
const dilution_calculate = async () => {
  if (!checkEmptyFields()) return;

  try {
    const requestData = {
      c1Value: convertEmptyToNull(c1.value),
      c1Unit: c1Unit.value,
      v1Value: convertEmptyToNull(v1.value),
      v1Unit: v1Unit.value,
      c2Value: convertEmptyToNull(c2.value),
      c2Unit: c2Unit.value,
      v2Value: convertEmptyToNull(v2.value),
      v2Unit: v2Unit.value,
    };

    const response = await fetch("http://localhost:8082/dilution_calculator", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();

    // 根据哪个字段为空来填充结果
    if (c1.value === "") {
      c1.value = result.calculatedValue;
      c1Unit.value = result.calculatedUnit;
    } else if (v1.value === "") {
      v1.value = result.calculatedValue;
      v1Unit.value = result.calculatedUnit;
    } else if (c2.value === "") {
      c2.value = result.calculatedValue;
      c2Unit.value = result.calculatedUnit;
    } else if (v2.value === "") {
      v2.value = result.calculatedValue;
      v2Unit.value = result.calculatedUnit;
    }

    Swal.fire({
      icon: "success",
      title: "Calculation Complete",
      text: `${result.message}`,
      showConfirmButton: true,
    });
  } catch (error) {
    console.error("Error:", error);
    Swal.fire({
      icon: "error",
      title: "Error",
      text: "An error occurred during calculation",
      footer: error.message,
    });
  }
};

const massCalculator = async () => {
  // Check if input is empty
  if (!molecularFormula.value.trim()) {
    Swal.fire({
      icon: "warning",
      title: "Input Cannot Be Empty",
      text: "Please enter a molecular formula",
    });
    return;
  }

  // Check if input contains only letters and numbers
  const regex = /^[a-zA-Z0-9]+$/;
  if (!regex.test(molecularFormula.value)) {
    Swal.fire({
      icon: "error",
      title: "Input Format Error",
      text: "The molecular formula can only contain letters and numbers",
    });
    return;
  }

  try {
    const response = await fetch("http://localhost:8082/mass_calculator", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        molecularFormula: molecularFormula.value,
      }),
    });

    const data = await response.json();
    totalMass.value = data.molecularWeight;

    Swal.fire({
      icon: "success",
      title: "Calculation Complete",
      text: `The molecular weight of ${molecularFormula.value} is: ${data.molecularWeight} ${data.unit}`,
    });
  } catch (error) {
    Swal.fire({
      icon: "error",
      title: "Error",
      text: "Please check if the molecular formula is correct",
      footer: error.message,
    });
    console.error("Error:", error);
  }
};
</script>

<style>

html::-webkit-scrollbar {
  display: none;
}

body.swal2-shown:not(.swal2-no-backdrop) {
  overflow: auto !important;
  padding-right: 0 !important;
}

input,
select {
  font-size: 14px;
}

.markdown-body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial,
    sans-serif;
  line-height: 1.6;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4 {
  margin-bottom: 10px;
  font-weight: 600;
}

.markdown-body h1 {
  font-size: 30px;
}

.markdown-body h2 {
  font-size: 22px;
}

.markdown-body h3 {
  font-size: 18px;
}

.markdown-body p {
  margin-bottom: 20px;
}

.markdown-body p img {
  display: block;
  margin: 0 auto;
}

.markdown-body pre {
  background-color: #f6f8fa;
  padding: 1em;
  border-radius: 4px;
  overflow: auto;
}

.markdown-body code {
  background-color: rgba(175, 184, 193, 0.2);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas,
    Liberation Mono, monospace;
}

/* 表格样式 */
.markdown-body table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
  overflow-x: auto;
  display: block;
}

.markdown-body th,
.markdown-body td {
  border: 1px solid #dfe2e5;
  padding: 0.5em 1em;
}

.markdown-body th {
  background-color: #f6f8fa;
  font-weight: 600;
}

.markdown-body tr {
  background-color: white;
}
</style>
