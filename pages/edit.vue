<template>
  <div>
    <!-- 从警告信息来看，img.vue 文件中存在一个 Vue 3 的常见问题：组件的模板没有单一的根节点 。Vue 3 虽然支持多根节点（即片段 Fragments），但在某些场景下（例如 Nuxt.js 的路由导航）仍然要求组件具有单一的根节点，否则可能会导致错误。 -->
    <nav class="bg-gray-800 text-white" style="background-color: black;">
      <div class="container px-6  py-3 flex justify-between items-center">
        <img src="/msbio_banner_logo.png" alt="Logo" class="h-10 w-auto" />
        <div class="flex space-x-4">
          <NuxtLink to="/volcano" class="text-[#CCCCCC] hover:text-white transition duration-300"
            active-class="text-blue-400">
            Volcano plot
          </NuxtLink>
        </div>
      </div>
    </nav>

    <div class="flex justify-center gap-[10vw] w-full">

      <div class="p-6 bg-white rounded-lg shadow-md mt-8 w-[30vw] h-full">
        <!-- 创建新文件夹 -->
        <div class="mb-8">
          <h3 class="text-xl font-semibold mb-4">Create New Folder</h3>
          <div class="flex items-center justify-center gap-4">
            <input v-model="newFolderName" placeholder="Enter folder name"
              class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500" />
            <!-- 调用 methods 方法 -->
            <button @click="createFolder" :disabled="isButtonDisabled()" :class="[
              'px-4 py-2 rounded-md focus:outline-none focus:ring-1 h-10 transition-all duration-500 ease-in-out',
              isButtonDisabled()
                ? 'bg-gray-300 text-gray-400 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-500'
            ]">
              Create
            </button>
          </div>
          <p v-if="createMessage" class="mt-2 text-sm text-green-600">{{ createMessage }}</p>
        </div>

        <!-- 选择已有文件夹 -->
        <div class="mb-8">
          <h3 class="text-xl font-semibold mb-4">Select Existing Folder</h3>
          <select v-model="selectedFolder" @change="handleFolderChange"
            class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500">

            <!-- <option v-for="folder in folders" :key="folder" :value="folder">{{ folder }}</option> -->

            <!-- 如果 folders 为空，则显示提示 -->
            <option v-if="folders.length === 0" disabled value="">No folders available, plz create one.</option>

            <!-- 动态生成文件夹选项 -->
            <option v-for="folder in folders" :key="folder" :value="folder">{{ folder }}</option>
          </select>
        </div>

        <!-- 显示图片名称 -->
        <div v-if="images.length" class="mb-8 mt-[-20px]">
          <ul>
            <li v-for="image in paginatedImages" :key="image"
              class="flex justify-between items-center p-2 border-b border-gray-200">
              <div class="flex-1 min-w-0 overflow-hidden">
                <p class="truncate">{{ image }}</p>
              </div>
              <div class="flex-shrink-0 ml-4 space-x-4">
                <button @click="viewImage(image)"
                  class="px-3 py-1 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-1 focus:ring-blue-500">
                  View
                </button>
                <button @click="deleteImage(image)"
                  class="px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-1 focus:ring-red-500">
                  Delete
                </button>
              </div>
            </li>
          </ul>

          <!-- 分页控件 -->
          <div class="flex justify-between items-center mt-2">
            <button @click="prevPage" :disabled="currentPage === 1"
              class="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed">
              Previous
            </button>
            <span>Page {{ currentPage }} of {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage === totalPages"
              class="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed">
              Next
            </button>
          </div>
        </div>

        <div v-if="selectedFolder && !images.length" class="mb-8 mt-[-20px]">
          <p class="text-gray-500 text-center">当前文件夹内容为空，请上传文件</p>
        </div>
        <div>
          <p v-if="deletedMessage" class="mb-4 mt-[-10px] text-sm text-red-600">{{ deletedMessage }}</p>
        </div>

        <!-- 上传图片 -->
        <!-- <div>
          <h3 class="text-xl font-semibold mb-4">Upload Image</h3>
          <div class="flex justify-center items-center gap-4">
            <input type="file" @change="onFileSelected"
              class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500" />
            <button @click="uploadImage" :disabled="isButton2Disabled()" :class="[
              'px-4 py-2 rounded-md focus:outline-none focus:ring-1 h-10 transition-all duration-500 ease-in-out',
              isButton2Disabled()
                ? 'bg-gray-300 text-gray-400 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-500'
            ]">
              Upload
            </button>
          </div>
          <p v-if="uploadMessage" class="mt-2 text-sm text-green-600">{{ uploadMessage }}</p>
        </div> -->

        <div>
          <h3 class="text-xl font-semibold mb-4">Upload Images</h3>
          <div class="flex justify-center items-center gap-4">
            <input type="file" @change="onFileSelected" multiple :disabled="isButton2Disabled()"
              class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500" />
            <button @click="uploadImages" :disabled="isButton2Disabled()" :class="[
              'px-4 py-2 rounded-md focus:outline-none focus:ring-1 h-10 transition-all duration-500 ease-in-out',
              isButton2Disabled()
                ? 'bg-gray-300 text-gray-400 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-500'
            ]">
              Upload
            </button>
          </div>
          <p v-if="uploadMessage" class="mt-2 text-sm text-green-600">{{ uploadMessage }}</p>
          <!-- <div v-if="uploadProgress > 0 && uploadProgress < 100" class="mt-2"> -->
          <div class="mt-2">
            <div class="w-full bg-gray-200 rounded-full h-2.5">
              <div class="bg-blue-600 h-2.5 rounded-full" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <p class="text-xs text-gray-500 mt-1">Uploading: {{ uploadProgress }}%</p>
          </div>
        </div>

      </div>

      <!-- Text Input and Output -->
      <div class="p-6 bg-gray-100 rounded-lg shadow-md w-[50vw] mt-8 h-[80vh] relative">
        <h3 class="text-xl font-semibold mb-4">Text Input and Output</h3>
        <textarea v-model="text_edited" placeholder="Type your report text here..."
          class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 resize-none h-[60vh]"></textarea>
        <button
          class="absolute bottom-4 right-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition duration-300"
          @click="handleUpload">
          Upload
        </button>
      </div>

      <!-- Modal for showing alert -->
      <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
        <div class="bg-white p-6 rounded-lg shadow-lg text-center">
          <p class="text-lg font-semibold mb-4">Please select a folder first!</p>
          <button class="bg-blue-500 text-white px-10 py-2 rounded-md hover:bg-blue-600 transition duration-300"
            @click="showModal = false">
            OK
          </button>
        </div>
      </div>

      <!-- 加载模态框 -->
      <div v-if="isLoading" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
        <div class="bg-white p-10 rounded-lg text-center">
          <div class="w-8 h-8 border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin mx-auto"></div>
          <p class="mt-2">Loading...</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
// 使用 useHead 设置页面标题
useHead({
  title: 'Edit',
  meta: [
    { name: 'description', content: '这是页面的描述内容' }
  ]
})
</script>

<script>
export default {
  data() {
    return {
      apiBaseUrl: "http://127.0.0.1:8081",
      newFolderName: "",
      createMessage: "",
      folders: [],
      selectedFolder: "",
      images: [],
      // selectedFile: null,
      selectedFiles: [],
      uploadMessage: "",
      deletedMessage: "",
      text_edited: "",
      showModal: false,
      isLoading: false,
      currentPage: 1,
      itemsPerPage: 6
    };
  },

  computed: {
    totalPages() {
      return Math.ceil(this.images.length / this.itemsPerPage);
    },
    paginatedImages() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.images.slice(start, end);
    }
  },

  methods: {
    isButtonDisabled() {
      return this.newFolderName.trim() === "";
    },
    isButton2Disabled() {
      return this.selectedFolder.trim() === "";
    },

    async createFolder() {
      try {
        const response = await fetch(`${this.apiBaseUrl}/create_folder/`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: `name=${encodeURIComponent(this.newFolderName)}`,
        });
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || "Failed to create folder.");
        }

        this.createMessage = data.message;
        this.loadFolders();
      } catch (error) {
        this.createMessage = error.message;
      }
    },
    async loadFolders() {
      try {
        const response = await fetch(`${this.apiBaseUrl}/list_folders/`);
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "Failed to load folders.");
        }

        this.folders = data.folders;
      } catch (error) {
        console.error("Error loading folders:", error);
      }
    },
    // async loadImages() {
    //   try {
    //     const response = await fetch(
    //       `${this.apiBaseUrl}/list_images/?folder_name=${encodeURIComponent(this.selectedFolder)}`
    //     );
    //     const data = await response.json();

    //     if (!response.ok) {
    //       throw new Error(data.detail || "Failed to load images.");
    //     }

    //     this.images = data.images;
    //   } catch (error) {
    //     console.error("Error loading images:", error);
    //   }
    // },
    // handleFolderChange() {
    //   this.loadImages();
    // },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    async loadImages() {
      try {
        const response = await fetch(
          `${this.apiBaseUrl}/list_images/?folder_name=${encodeURIComponent(this.selectedFolder)}`
        );
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "Failed to load images.");
        }

        this.images = data.images;
        this.currentPage = 1; // 重置到第一页
      } catch (error) {
        console.error("Error loading images:", error);
      }
    },
    handleFolderChange() {
      this.loadImages();
    },

    // onFileSelected(event) {
    //   this.selectedFile = event.target.files[0];
    // },

    onFileSelected(event) {
      this.selectedFiles = Array.from(event.target.files); // 获取所有选中的文件数组
      console.log(this.selectedFiles)
    },
    // 上传单个文件
    // async uploadImage() {
    //   if (!this.selectedFile) {
    //     this.uploadMessage = "Please select a file first.";
    //     return;
    //   }

    //   const formData = new FormData();
    //   formData.append("folder_name", this.selectedFolder);
    //   formData.append("file", this.selectedFile);

    //   try {
    //     const response = await fetch(`${this.apiBaseUrl}/upload_image/`, {
    //       method: "POST",
    //       body: formData,
    //     });
    //     const data = await response.json();

    //     if (!response.ok) {
    //       throw new Error(data.detail || "Failed to upload image.");
    //     }

    //     this.uploadMessage = data.message;
    //     this.loadImages();
    //   } catch (error) {
    //     this.uploadMessage = error.message;
    //   }
    // },

    async uploadImages() {
      if (this.selectedFiles.length === 0) {
        this.uploadMessage = "Please select at least one file first.";
        return;
      }

      this.uploadProgress = 0;
      const progressIncrement = 100 / this.selectedFiles.length;

      try {
        const results = [];

        for (const [index, file] of this.selectedFiles.entries()) {
          const formData = new FormData();
          formData.append("folder_name", this.selectedFolder);
          formData.append("files", file); // 注意后端接收的是files

          const response = await fetch(`${this.apiBaseUrl}/upload_images/`, {
            method: "POST",
            body: formData,
          });

          const data = await response.json();

          if (!response.ok) {
            throw new Error(data.detail || `Failed to upload file: ${file.name}`);
          }

          results.push(data.message);
          this.uploadProgress = (index + 1) * progressIncrement;
        }

        this.uploadMessage = `Successfully uploaded ${this.selectedFiles.length} files.`;
        this.loadImages();
      } catch (error) {
        this.uploadMessage = error.message;
      } finally {
        this.selectedFiles = [];
      }
    },


    async deleteImage(imageName) {
      try {
        const response = await fetch(`${this.apiBaseUrl}/delete_image/`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            folder_name: this.selectedFolder,
            image_name: imageName,
          }),
        });
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "Failed to delete image.");
        }

        this.deletedMessage = data.message;
        this.loadImages();
      } catch (error) {
        this.deletedMessage = error.message;
      }
    },
    // async viewImage(imageName) {
    //   try {
    //     // 请求图片 Blob 数据
    //     const response = await fetch(`${this.apiBaseUrl}/view_image/`, {
    //       method: "POST",
    //       headers: { "Content-Type": "application/json" },
    //       body: JSON.stringify({
    //         folder_name: this.selectedFolder,
    //         image_name: imageName,
    //       }),
    //     });

    //     if (!response.ok) {
    //       throw new Error("Failed to fetch image.");
    //     }

    //     // 将响应转换为 Blob
    //     const blob = await response.blob();

    //     // 创建一个临时 URL
    //     const imageUrl = URL.createObjectURL(blob);

    //     // 在新页面中打开图片
    //     window.open(imageUrl, "_blank");
    //   } catch (error) {
    //     this.uploadMessage = error.message;
    //   }
    // },
    async viewImage(imageName) {
      try {
        // 请求文件 Blob 数据
        const response = await fetch(`${this.apiBaseUrl}/view_image/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            folder_name: this.selectedFolder,
            image_name: imageName,
          }),
        });

        if (!response.ok) {
          throw new Error("Failed to fetch file.");
        }

        // 将响应转换为 Blob
        const blob = await response.blob();

        // 获取 MIME 类型
        const mimeType = response.headers.get('content-type');

        // 检查是否是图片文件
        if (mimeType && mimeType.startsWith('image/')) {
          // 如果是图片文件，则在新页面中打开
          const imageUrl = URL.createObjectURL(blob);
          window.open(imageUrl, "_blank");
        } else {
          // 如果不是图片文件，则直接下载
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = imageName;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
        }
      } catch (error) {
        this.uploadMessage = error.message;
      }
    },
    async handleUpload() {
      // 显示 loading 模态框
      this.isLoading = true;

      // 检查 selectedFolder 是否存在
      if (!this.selectedFolder) {
        // 取消 loading 模态框
        this.isLoading = false;
        // 显示提示模态框
        this.showModal = true;
        return;
      }

      try {
        const blob = new Blob([this.text_edited], { type: 'text/plain' });

        const formData = new FormData();
        formData.append('txt_file', blob, 'report_editd.txt');
        formData.append('img_folder', this.selectedFolder);
        console.log(this.selectedFolder, formData);

        const response = await fetch('http://127.0.0.1:8081/upload-txt', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const blob = await response.blob();

          // 创建一个临时的 <a> 标签来触发下载
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'converted_report.zip';
          document.body.appendChild(a);
          a.click(); // 触发点击事件以开始下载
          a.remove(); // 移除 <a> 标签
          window.URL.revokeObjectURL(url);
          alert('File downloaded successfully!');
        } else {
          alert('Failed to upload file.');
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        alert('An error occurred while uploading the file.');
      } finally {
        // 无论成功与否，都要取消 loading 模态框
        this.isLoading = false;
      }
    },
    async handleUpload() {
      if (!this.selectedFolder) {
        this.showModal = true;
        return;
      }

      try {
        const blob = new Blob([this.text_edited], { type: 'text/plain' });

        const formData = new FormData();
        formData.append('txt_file', blob, 'report_editd.txt');
        formData.append('img_folder', this.selectedFolder);
        console.log(this.selectedFolder, formData)
        const response = await fetch('http://127.0.0.1:8081/upload-txt', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const blob = await response.blob();

          // 创建一个临时的 <a> 标签来触发下载
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'converted_report.zip';
          document.body.appendChild(a);
          a.click(); // 触发点击事件以开始下载
          a.remove(); // 移除 <a> 标签
          window.URL.revokeObjectURL(url);
          alert('File downloaded successfully!');
        } else {
          alert('Failed to upload file.');
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        alert('An error occurred while uploading the file.');
      }
    },
  },

  mounted() {
    this.loadFolders();
  },

};
</script>

<!-- <style scoped>
.absolute {
  position: absolute;
}
</style> -->
