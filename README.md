# LLM_URL_Generator  

基于 Flask 和 MinIO 的课程资源链接生成服务，通过课程名称查询并生成 MinIO 预签名下载链接。  


## 功能特点  
- 接收课程名称，通过 CSV 匹配课程信息  
- 生成 MinIO 对象存储的预签名下载链接（有效期 1 小时）  
- 支持 HTTP API 调用，返回 JSON 格式结果  


## 环境要求  
- **Python 3.7+**  
- 依赖库：  
  ```bash  
  flask          # Web 框架  
  minio          # MinIO 客户端  
