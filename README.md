# 进入你希望放仓库的目录
cd ~/你的工作目录

# 创建主文件夹
mkdir ai-robot-진서용
cd ai-robot-진서용

# 创建空 README
touch README.md

# 创建 16 周文件夹及截图子文件夹和安装记录.md
for i in $(seq 1 16)
do
  mkdir -p week$i/截图
  touch week$i/安装记录.md
done
