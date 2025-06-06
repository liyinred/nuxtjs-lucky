<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-4">
            <img src="/portal/logo.png" class="h-20 w-auto" />
            <div>
              <h1 class="text-3xl font-bold text-gray-900">MSBIO Lab Portal</h1>
              <p class="mt-1 text-sm text-gray-500">
                Laboratory L02 - Documents and Tools
              </p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <button class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">
              Notifications
            </button>
            <!-- <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center">
              <span class="text-gray-600 font-medium">JD</span>
            </div> -->
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
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

      <!-- Chemistry Tools Modal -->
      <div v-if="showChemistryModal" @click.self="closeModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-auto">
          <div class="p-6">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-gray-800">化学计算工具</h2>
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
                    <div class="flex items-center justify-center space-x-2 mb-4">
                      <!-- Mass 输入框 -->
                      <div class="flex items-center">
                        <input v-model.number="mass" type="number"
                          class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          placeholder="Mass" />
                        <select v-model="massUnit"
                          class="ml-2 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                          <option value="mg">mg</option>
                          <option value="g">g</option>
                          <option value="kg">kg</option>
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
                          <option value="mM">mM</option>
                          <option value="M">M</option>
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
                          <option value="μL">μL</option>
                          <option value="mL">mL</option>
                          <option value="L">L</option>
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
                    <div class="flex justify-end space-x-2 mt-6">
                      <button @click="reset1"
                        class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400">
                        重置
                      </button>
                      <button @click="calculate"
                        class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400">
                        计算
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
                  <div class="bg-white p-10 rounded-lg shadow-sm">
                    <!-- 第一行：输入框和计算按钮 -->
                    <div class="flex space-x-2 mb-4">
                      <input v-model="molecularFormula" type="text" placeholder="请输入分子式(如H2O)"
                        class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
                      <button @click="massCalculator"
                        class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500">
                        计算
                      </button>
                    </div>

                    <!-- 第二行：总分子量显示 -->
                    <div class="flex items-center">
                      <label class="mr-2 text-gray-700">总分子量:</label>
                      <input :value="totalMass" readonly
                        class="px-3 py-2 border border-gray-300 rounded-md bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500" />
                      <span class="ml-2 text-gray-700">g/mol</span>
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
                    <!-- 输入框行 -->
                    <div class="flex items-center justify-center space-x-2 mb-4">
                      <!-- 初始溶液 -->
                      <div class="flex items-center justify-center space-x-2">
                        <div class="flex items-center">
                          <input v-model.number="c1" type="number"
                            class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="C1" />
                          <select v-model="c1Unit"
                            class="ml-2 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="μM">μM</option>
                            <option value="mM">mM</option>
                            <option value="M">M</option>
                          </select>
                        </div>

                        <span class="mx-2 text-gray-600 font-bold">×</span>

                        <div class="flex items-center">
                          <input v-model.number="v1" type="number"
                            class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="V1" />
                          <select v-model="v1Unit"
                            class="ml-2 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="μL">μL</option>
                            <option value="mL">mL</option>
                            <option value="L">L</option>
                          </select>
                        </div>
                      </div>

                      <!-- 等号 -->
                      <div class="flex justify-center">
                        <span class="mx-2 text-gray-600 font-bold">=</span>
                      </div>

                      <!-- 稀释后溶液 -->
                      <div class="flex items-center justify-center space-x-2">
                        <div class="flex items-center">
                          <input v-model.number="c2" type="number"
                            class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="C2" />
                          <select v-model="c2Unit"
                            class="ml-2 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="μM">μM</option>
                            <option value="mM">mM</option>
                            <option value="M">M</option>
                          </select>
                        </div>

                        <span class="mx-2 text-gray-600 font-bold">×</span>

                        <div class="flex items-center">
                          <input v-model.number="v2" type="number"
                            class="w-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="V2" />
                          <select v-model="v2Unit"
                            class="ml-2 px-2 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="μL">μL</option>
                            <option value="mL">mL</option>
                            <option value="L">L</option>
                          </select>
                        </div>
                      </div>
                    </div>

                    <!-- 按钮区域 -->
                    <div class="flex justify-end space-x-2 mt-6">
                      <button @click="reset2"
                        class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400">
                        重置
                      </button>
                      <button @click="dilution_calculate"
                        class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400">
                        计算
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

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

useHead({
  title: "MSBIO Portal",
});

const documents = ref([
  {
    id: 1,
    title: "Biotech Cleaning Schedule",
    category: "Cleaning",
    date: "2025-06-03",
    image: "/portal/L02_Biotech_Cleaning_Schedule-1.png",
  },
  {
    id: 2,
    title: "Cleaning Checklist",
    category: "Cleaning",
    date: "2025-06-03",
    image: "/portal/L02_Cleaning_Checklist-1.png",
  },
  {
    id: 3,
    title: "Safety Checklist",
    category: "Safety",
    date: "2025-06-03",
    image: "/portal/L02_Safety_Checklist-1.png",
  },
  {
    id: 4,
    title: "Sanitation Duty Schedule",
    category: "Schedule",
    date: "2025-06-03",
    image: "/portal/L02_Sanitation Duty Schedule (May-June)-1.png",
  },
  {
    id: 5,
    title: "化学计算工具",
    category: "Tool",
    date: "2025-06-06", // 改为YYYY-MM-DD格式
    image: "/portal/logo.png",
  },
]);

// 计算上海时间与给定日期的天数差
const formatUpdatedDate = (dateString) => {
  if (!dateString || isNaN(new Date(dateString))) {
    return "Invalid date";
  }

  try {
    // 获取上海时区的当前日期(00:00:00)
    const options = { timeZone: 'Asia/Shanghai' };
    const todayStr = new Date().toLocaleDateString('en-US', options);
    const today = new Date(todayStr);

    // 解析输入日期并转换为上海时区日期
    const inputDate = new Date(dateString);
    const inputDateStr = inputDate.toLocaleDateString('en-US', options);
    const shanghaiInputDate = new Date(inputDateStr);

    // 计算天数差
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

    const response = await fetch("http://192.168.10.96:8082/molarity_calculator", {
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
      title: "Success",
      text: "The calculation was performed successfully!",
      timer: 2000,
      showConfirmButton: false,
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

// 计算函数
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

    const response = await fetch("http://192.168.10.96:8082/dilution_calculator", {
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
      text: "The calculation was performed successfully!",
      timer: 2000,
      showConfirmButton: false,
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
    const response = await fetch("http://192.168.10.96:8082/mass_calculator", {
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
      text: `${molecularFormula.value} 的分子量为: ${data.molecularWeight} ${data.unit}`,
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

const handleCardClick = (document, event) => {
  if (document.title === "化学计算工具") {
    event.preventDefault();
    showChemistryModal.value = true;
  }
};

const closeModal = () => {
  showChemistryModal.value = false;
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
    const categoryMatch =
      selectedCategories.value.includes("All") ||
      selectedCategories.value.includes(doc.category);

    const searchMatch =
      doc.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      doc.category.toLowerCase().includes(searchQuery.value.toLowerCase());

    return categoryMatch && searchMatch;
  });
});
</script>

<!-- <script>
import { ref, computed } from 'vue';

export default {
  setup() {

    useHead({
      title: 'MSBIO Portal'
    })

    const documents = ref([
      {
        id: 1,
        title: 'Biotech Cleaning Schedule',
        category: 'Cleaning',
        date: 'Updated 2 days ago',
        image: 'L02_Biotech_Cleaning_Schedule-1.png'
      },
      {
        id: 2,
        title: 'Cleaning Checklist',
        category: 'Cleaning',
        date: 'Updated 1 week ago',
        image: 'L02_Cleaning_Checklist-1.png'
      },
      {
        id: 3,
        title: 'Safety Checklist',
        category: 'Safety',
        date: 'Updated 3 days ago',
        image: 'L02_Safety_Checklist-1.png'
      },
      {
        id: 4,
        title: 'Sanitation Duty Schedule',
        category: 'Schedule',
        date: 'Updated 1 month ago',
        image: 'L02_Sanitation Duty Schedule (May-June)-1.png'
      }
    ]);

    const categories = ref(['All', 'Cleaning', 'Safety', 'Schedule']);
    const selectedCategories = ref(['All']);
    const searchQuery = ref('');

    const toggleCategory = (category) => {
      if (category === 'All') {
        selectedCategories.value = ['All'];
      } else {
        // Remove 'All' if other categories are selected
        if (selectedCategories.value.includes('All')) {
          selectedCategories.value = selectedCategories.value.filter(c => c !== 'All');
        }

        if (selectedCategories.value.includes(category)) {
          selectedCategories.value = selectedCategories.value.filter(c => c !== category);
          // If no categories selected, show all
          if (selectedCategories.value.length === 0) {
            selectedCategories.value = ['All'];
          }
        } else {
          selectedCategories.value.push(category);
        }
      }
    };

    const filteredDocuments = computed(() => {
      return documents.value.filter(doc => {
        // Filter by category
        const categoryMatch = selectedCategories.value.includes('All') ||
          selectedCategories.value.includes(doc.category);

        // Filter by search query
        const searchMatch = doc.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          doc.category.toLowerCase().includes(searchQuery.value.toLowerCase());

        return categoryMatch && searchMatch;
      });
    });

    return {
      documents,
      categories,
      selectedCategories,
      searchQuery,
      toggleCategory,
      filteredDocuments
    };
  }
};
</script> -->
