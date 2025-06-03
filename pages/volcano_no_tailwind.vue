<template>
  <div class="container">
    <!-- 文件上传 -->
    <div class="file-upload">
      <label for="fileInput" class="upload-label">
        📂 选择 CSV 文件
      </label>
      <input type="file" id="fileInput" @change="handleFileChange" accept=".csv" class="hidden-input" />
      <div v-if="fileName" style="font-size: 12px;margin-top: 5px;">
        已选择文件: {{ fileName }}
      </div>
      <div style="font-size: 12px; color: #666; margin-top: 5px;">
        CSV 文件的列名中必须要有 "-10log10P", "Log2FC", "Gene"
      </div>
    </div>

    <!-- 表单输入 -->
    <div class="form-group">
      <label for="sig_level" class="form-label">显著性水平 (Sig Level):</label>
      <input type="number" id="sig_level" v-model="form.sig_level" step="0.01" class="form-input" />
    </div>

    <div class="form-group">
      <label for="fold_level" class="form-label">倍数变化阈值 (Fold Level):</label>
      <input type="number" id="fold_level" v-model="form.fold_level" step="0.01" class="form-input" />
    </div>

    <div class="form-group">
      <label for="title" class="form-label">图表标题 (Title):</label>
      <input type="text" id="title" v-model="form.title" class="form-input" />
    </div>

    <div style="display: flex;gap: 20px;">
      <div class="form-group" style="display: flex;align-items: center;">
        <label for="annotate_gene" class="form-label" style="margin: 0;">标注基因:</label>
        <input type="checkbox" id="annotate_gene" v-model="form.annotate_gene" @change="handleAnnotateChange('gene')"
          class="form-checkbox" style="width: 20px;height: 20px;margin-left: 10px;" />
      </div>

      <div class="form-group" style="display: flex;align-items: center;">
        <label for="annotate_protein" class="form-label" style="margin: 0;">标注蛋白:</label>
        <input type="checkbox" id="annotate_protein" v-model="form.annotate_protein"
          @change="handleAnnotateChange('protein')" class="form-checkbox"
          style="width: 20px;height: 20px;margin-left: 10px;" />
      </div>
    </div>

    <!-- 新增 highlighted_normal_points 参数 -->
    <div class="form-group" style="display: flex;align-items: center;">
      <label for="highlighted_normal_points" class="form-label" style="margin: 0;">显示显著点标签:</label>
      <input type="checkbox" id="highlighted_normal_points" v-model="form.highlighted_normal_points"
        class="form-checkbox" style="width: 20px;height: 20px;margin-left: 10px;" />
    </div>

    <!-- 新增 highlighted_genes 参数 -->
    <div class="form-group">
      <label for="highlighted_genes" class="form-label">高亮基因/蛋白:</label>
      <input type="text" id="highlighted_genes" v-model="form.highlighted_genes" class="form-input"
        placeholder="输入基因名称或者蛋白名称，用逗号分隔" />
    </div>

    <button @click="uploadFile" class="submit-button">
      上传并提交
    </button>

    <div v-if="isLoading" class="loading-modal">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <p>Loading</p>
      </div>
    </div>

    <div v-if="imageUrl" class="chart-container">
      <h3 class="chart-title" style="text-align: left;">生成的火山图:</h3>
      <img :src="imageUrl" alt="Volcano Plot" class="chart-image" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        sig_level: 13.01,
        fold_level: 0.585,
        title: "Volcano Plot",
        highlighted_normal_points: true, // 默认值为 true
        highlighted_genes: "", // 默认值为空字符串
        annotate_gene: true, // 默认选择标注基因
        annotate_protein: false, // 默认不选择标注蛋白
      },
      file: null,
      fileName: "",
      imageUrl: "",
      isLoading: false,
    };
  },
  methods: {
    handleFileChange(event) {
      this.file = event.target.files[0]; // 获取用户选择的文件
      this.fileName = this.file ? this.file.name : ""; // 更新文件名
    },
    // 处理标注类型的变化
    handleAnnotateChange(type) {
      if (type === "gene") {
        // 如果选择了标注基因，则取消标注蛋白的选择
        if (this.form.annotate_gene) {
          this.form.annotate_protein = false;
        } else {
          // 如果取消标注基因，则强制选择标注蛋白
          this.form.annotate_protein = true;
        }
      } else if (type === "protein") {
        // 如果选择了标注蛋白，则取消标注基因的选择
        if (this.form.annotate_protein) {
          this.form.annotate_gene = false;
        } else {
          // 如果取消标注蛋白，则强制选择标注基因
          this.form.annotate_gene = true;
        }
      }
    },
    async uploadFile() {
      if (!this.file) {
        alert("请先选择文件");
        return;
      }

      this.isLoading = true; // 显示加载模态框

      const formData = new FormData();
      formData.append("file", this.file);
      formData.append("sig_level", this.form.sig_level);
      formData.append("fold_level", this.form.fold_level);
      formData.append("title", this.form.title);
      formData.append("highlighted_normal_points", this.form.highlighted_normal_points);
      formData.append("highlighted_genes", this.form.highlighted_genes);

      // 根据选择的标注类型确定上传的URL
      const uploadUrl = this.form.annotate_gene ? "/upload/volcano-gene" : "/upload/volcano-protein";

      try {
        const response = await fetch(`http://127.0.0.1:8081${uploadUrl}`, {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error("上传失败");
        }

        const blob = await response.blob(); // 获取返回的图片 Blob
        const imageUrl = URL.createObjectURL(blob); // 生成图片 URL
        this.imageUrl = imageUrl; // 更新图片 URL

        // 直接在新页面中打开图片 URL
        window.open(imageUrl, '_blank');

      } catch (error) {
        console.error("上传失败:", error);
        alert("上传失败，请重试");
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>
<style scoped>
.container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.file-upload {
  text-align: center;
  margin-bottom: 20px;
}

.upload-label {
  display: inline-block;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.upload-label:hover {
  background-color: #0056b3;
}

.hidden-input {
  display: none;
}

/* 表单样式 */
.form-group {
  margin-bottom: 15px;
}

.form-label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.form-input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

/* 提交按钮样式 */
.submit-button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #218838;
}

/* 图表容器样式 */
.chart-container {
  margin-top: 20px;
  text-align: center;
}

.chart-title {
  font-size: 18px;
  color: #333;
  margin-bottom: 10px;
}

.chart-image {
  max-width: 100%;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.loading-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-content {
  background-color: white;
  padding: 40px;
  border-radius: 5px;
  text-align: center;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 0 auto 10px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
