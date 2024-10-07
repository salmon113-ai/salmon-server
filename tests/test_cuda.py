import torch

# PyTorch 버전 확인
print(f"PyTorch 버전: {torch.__version__}")

# CUDA 사용 가능 여부 확인
print(f"CUDA 사용 가능: {torch.cuda.is_available()}")

# 사용 가능한 GPU 개수 확인
print(f"사용 가능한 GPU 개수: {torch.cuda.device_count()}")

# 현재 GPU 이름 확인 (CUDA 사용 가능한 경우)
if torch.cuda.is_available():
    print(f"현재 GPU: {torch.cuda.get_device_name(0)}")

# 간단한 텐서 연산 테스트
x = torch.rand(5, 3)
print(f"랜덤 텐서:\n{x}")

# GPU 사용 가능 시 GPU로 텐서 이동
if torch.cuda.is_available():
    x = x.to('cuda')
    print(f"GPU로 이동된 텐서:\n{x}")

# 행렬 곱 연산 테스트
y = torch.rand(3, 4)
if torch.cuda.is_available():
    y = y.to('cuda')
z = torch.mm(x, y)
print(f"행렬 곱 결과:\n{z}")